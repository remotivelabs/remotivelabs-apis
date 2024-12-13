from __future__ import annotations

import binascii
import json
import queue
from threading import Thread
from typing import Callable, Iterable, List, Optional, Union

import grpc

from .. import network_api_pb2 as network_api
from .. import (
    network_api_pb2_grpc,
    system_api_pb2_grpc,
    traffic_api_pb2_grpc,
)
from . import helper as br
from .signalcreator import SignalCreator


class SignalValue:
    """
    Wrapper around protobuf generated class to make it a bit simpler to use
    to make us learn how we want the next version of the API to look like.

    Use the signal.is_{type}() functions to validate type before you get value.
    Use signal.value() to get the actual value without any validation.
    Use signal.get_raw() to get the raw bytes
    Use signal.{type}_value() to get a validated typed value or error if something is wrong
    """

    def __init__(self, signal: network_api.Signal):
        self.signal: network_api.Signal = signal

    def __str__(self):
        return self.to_json()

    def to_json(self) -> str:
        return json.dumps(self.as_dict())

    def is_integer(self) -> bool:
        return self.signal.HasField("integer")

    def is_double(self) -> bool:
        return self.signal.HasField("double")

    def is_arbitration(self) -> bool:
        return self.signal.HasField("arbitration")

    def is_raw(self) -> bool:
        return self.signal.raw != b""

    def get_raw(self) -> Union[bytes, None]:
        if self.is_raw():
            return self.signal.raw
        return None

    def __get_value(self) -> Union[str, int, float, bool, None]:
        if self.signal.raw != b"":
            return "0x" + binascii.hexlify(self.signal.raw).decode("ascii")
        if self.signal.HasField("integer"):
            return self.signal.integer
        if self.signal.HasField("double"):
            return self.signal.double
        if self.signal.HasField("arbitration"):
            return self.signal.arbitration
        return None

    def timestamp_us(self):
        return self.signal.timestamp

    def name(self):
        return self.signal.id.name

    def namespace(self):
        return self.signal.id.namespace.name

    def value(self):
        return self.__get_value()

    def __get_with_ensured_type(self, t: type):
        v = self.__get_value()
        if isinstance(v, t):
            return v
        raise BrokerException(f"{v} was not expected type '{t}' but got '{type(v)}'")

    def float_value(self):
        return self.__get_with_ensured_type(float)

    def int_value(self):
        return self.__get_with_ensured_type(int)

    def bool_value(self):
        return self.__get_with_ensured_type(bool)

    def bytes_value(self):
        return self.__get_with_ensured_type(bytes)

    def as_dict(self):
        return {
            "timestamp_us": self.timestamp_us(),
            "name": self.name(),
            "namespace": self.namespace(),
            "value": self.value(),
        }


class SignalsInFrame(Iterable):
    def __init__(self, signals: List[SignalValue]):
        self.signals = signals
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.signals[self.index]
        except IndexError as ex:
            raise StopIteration from ex
        self.index += 1
        return result


class SignalIdentifier:
    def __init__(self, name: str, namespace: str):
        self.name = name
        self.namespace = namespace

    @staticmethod
    def parse(signal_id: str) -> SignalIdentifier:
        s = signal_id.split(":")
        if len(s) != 2:
            raise BrokerException("signal names must have format namespace:signal_name")
        return SignalIdentifier(s[1], s[0])


class BrokerException(Exception):  # noqa: N818
    pass


# pylint: disable=too-many-instance-attributes
class Client:
    def __init__(self, client_id: str = "broker_client"):
        self._signal_creator: SignalCreator
        self._traffic_stub: traffic_api_pb2_grpc.TrafficServiceStub
        self._system_stub: system_api_pb2_grpc.SystemServiceStub
        self._network_stub: network_api_pb2_grpc.NetworkServiceStub
        self._intercept_channel: grpc.Channel
        self.client_id = client_id
        self.url: Optional[str] = None
        self.api_key: Optional[str] = None
        self.on_connect: Union[Callable[[Client], None], None] = None
        self.on_signals: Union[Callable[[SignalsInFrame], None], None] = None

    def connect(self, url: str, api_key: Union[str, None] = None, max_message_length: Union[int, None] = None):
        self.url = url
        self.api_key = api_key
        if url.startswith("https"):
            if api_key is None:
                raise BrokerException("You must supply api-key or access-token to use a cloud broker")
            self._intercept_channel = br.create_channel(url, self.api_key, None, max_message_length)
        else:
            self._intercept_channel = br.create_channel(url, None, None, max_message_length)

        self._network_stub = network_api_pb2_grpc.NetworkServiceStub(self._intercept_channel)
        self._system_stub = system_api_pb2_grpc.SystemServiceStub(self._intercept_channel)
        self._traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(self._intercept_channel)
        self._signal_creator = SignalCreator(self._system_stub)
        if self.on_connect is not None:
            self.on_connect(self)

    def subscribe(
        self,
        signals_to_subscribe_to: List[SignalIdentifier],
        on_signals: Optional[Callable[[SignalsInFrame], None]] = None,
        changed_values_only: bool = True,
    ):
        client_id = br.common_pb2.ClientId(id="subscribe-sample")
        if on_signals is None and self.on_signals is None:
            raise BrokerException(
                "You have not specified global client.on_signals nor client.subscribe(on_signals=callback), "
                "or you are invoking subscribe() before client.on_signals which is not allowed"
            )

        def to_protobuf_signal(s: SignalIdentifier):
            return self._signal_creator.signal(s.name, s.namespace)

        _signals_to_subscribe_on = list(map(to_protobuf_signal, signals_to_subscribe_to))
        wait_for_subscription_queue: queue.Queue = queue.Queue()
        Thread(
            target=br.act_on_signal,
            args=(
                client_id,
                self._network_stub,
                _signals_to_subscribe_on,
                changed_values_only,  # True: only report when signal changes
                lambda frame: self._on_signals(frame, on_signals),
                lambda sub: (wait_for_subscription_queue.put((self.client_id, sub))),
            ),
        ).start()

        client_id, subscription = wait_for_subscription_queue.get()
        return subscription

    def _on_signals(self, signals_in_frame: network_api.Signals, callback):
        """
        Updates "local" callback or global on_signals callback if local callback is None
        """
        if callback is not None:
            callback(SignalsInFrame(list(map(SignalValue, signals_in_frame))))  # type: ignore[call-overload]
        elif self.on_signals is not None:
            self.on_signals(SignalsInFrame(list(map(SignalValue, signals_in_frame))))  # type: ignore[call-overload]

    def list_signal_names(self) -> List[SignalIdentifier]:
        configuration = self._system_stub.GetConfiguration(br.common_pb2.Empty())

        signal_names: List[SignalIdentifier] = []
        for network_info in configuration.networkInfo:
            res = self._system_stub.ListSignals(network_info.namespace)
            for finfo in res.frame:
                # f: br.common_pb2.FrameInfo = finfo
                signal_names.append(SignalIdentifier(finfo.signalInfo.id.name, network_info.namespace.name))
                for sinfo in finfo.childInfo:
                    signal_names.append(SignalIdentifier(sinfo.id.name, network_info.namespace.name))
        return signal_names
