#!/usr/bin/env python3

import binascii
import json
import queue
from threading import Thread
from typing import Union, Callable, List, Iterable

from . import SignalCreator
from . import helper as br
from ..generated.sync import network_api_pb2 as network_api
from ..generated.sync import network_api_pb2_grpc
from ..generated.sync import system_api_pb2_grpc
from ..generated.sync import traffic_api_pb2_grpc


class SignalWrapper:
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
        else:
            return None

    def __get_value(self) -> Union[str, int, float, bool, None]:
        if self.signal.raw != b"":
            return "0x" + binascii.hexlify(self.signal.raw).decode("ascii")
        elif self.signal.HasField("integer"):
            return self.signal.integer
        elif self.signal.HasField("double"):
            return self.signal.double
        elif self.signal.HasField("arbitration"):
            return self.signal.arbitration
        else:
            return None

    def timestamp_us(self):
        return self.signal.timestamp

    def name(self):
        return self.signal.id.name

    def namespace(self):
        return self.signal.id.namespace.name

    def value(self):
        return self.__get_value()

    def float_value(self):
        v = self.__get_value()
        if isinstance(v, float):
            return v
        else:
            raise BrokerException(f"{v} was not expected type float but got {type(v)}")

    def int_value(self):
        v = self.__get_value()
        if isinstance(v, int):
            return v
        else:
            raise BrokerException(f"{v} was not expected type int but got {type(v)}")

    def bool_value(self):
        v = self.__get_value()
        if isinstance(v, bool):
            return v
        else:
            raise BrokerException(f"{v} was not expected type bool but got {type(v)}")

    def bytes_value(self):
        v = self.__get_value()
        if isinstance(v, bytes):
            return v
        else:
            raise BrokerException(f"{v} was not expected type bytes but got {type(v)}")

    def as_dict(self):
        return {
            'timestamp_us': self.timestamp_us(),
            'name': self.name(),
            'namespace': self.namespace(),
            'value': self.value()
        }


class SignalsInFrame(Iterable):

    def __init__(self, signals: list[SignalWrapper]):
        self.signals = signals
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.signals[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result


class SignalIdentifier:
    def __init__(self, name: str, namespace: str):
        self.name = name
        self.namespace = namespace


class BrokerException(Exception):
    pass


class Client:

    def __init__(self, client_id: str = "broker_client"):

        self._signal_creator = None
        self._traffic_stub = None
        self._system_stub = None
        self._network_stub = None
        self._intercept_channel = None
        self.client_id = client_id
        self.url = None
        self.api_key = None
        self.on_connect: Union[Callable[[Client], None], None] = None
        self.on_signals: Union[Callable[[SignalsInFrame], None], None] = None

    def connect(self,
                url: str,
                api_key: Union[str, None] = None):
        self.url = url
        self.api_key = api_key
        if url.startswith("https"):
            if api_key is None:
                raise BrokerException("You must supply api-key or access-token to use a cloud broker")
            self._intercept_channel = br.create_channel(url, self.api_key, None)
        else:
            self._intercept_channel = br.create_channel(url, None, None)

        self._network_stub = network_api_pb2_grpc.NetworkServiceStub(self._intercept_channel)
        self._system_stub = system_api_pb2_grpc.SystemServiceStub(self._intercept_channel)
        self._traffic_stub = traffic_api_pb2_grpc.TrafficServiceStub(self._intercept_channel)
        self._signal_creator = SignalCreator(self._system_stub)
        if self.on_connect is not None:
            self.on_connect(self)

    def _validate_and_get_subscribed_signals(self, subscribed_namespaces: List[str], subscribed_signals: List[str]) \
            -> List[SignalIdentifier]:
        # Since we cannot know which list[signals] belongs to which namespace we need to fetch
        # all signals from the broker and find the proper signal with namespace. Finally,  we
        # also filter out namespaces that we do not need since we might have duplicated signal names
        # over namespaces
        # Begin

        def verify_namespace(available_signal: SignalIdentifier):
            return list(filter(lambda namespace: available_signal.namespace == namespace, subscribed_namespaces))

        def find_subscribed_signal(available_signal: SignalIdentifier):
            return list(filter(lambda s: available_signal.name == s, subscribed_signals))

        available_signals: list[SignalIdentifier] = list(filter(verify_namespace, self.list_signal_names()))
        signals_to_subscribe_to: list[SignalIdentifier] = list(filter(find_subscribed_signal, available_signals))

        # Check if subscription is done on signal that is not in any of these namespaces
        signals_subscribed_to_but_does_not_exist = \
            set(subscribed_signals) - set(map(lambda s: s.name, signals_to_subscribe_to))

        if len(signals_subscribed_to_but_does_not_exist) > 0:
            raise BrokerException(f"One or more signals you subscribed to does not exist "
                                  f", {signals_subscribed_to_but_does_not_exist}")

        return list(map(lambda s: SignalIdentifier(s.name, s.namespace), signals_to_subscribe_to))

    def subscribe(self,
                  signal_names: list[str],
                  namespaces: list[str],
                  on_signals: Callable[[SignalsInFrame], None] = None,
                  changed_values_only: bool = True):

        if on_signals is None and self.on_signals is None:
            raise BrokerException(
                "You have not specified global client.on_signals nor client.subscribe(on_signals=callback), "
                "or you are invoking subscribe() before client.on_signals which is not allowed")

        client_id = br.common_pb2.ClientId(id=self.client_id)
        signals_to_subscribe_to: List[SignalIdentifier] = self._validate_and_get_subscribed_signals(
            namespaces,
            signal_names)

        def to_protobuf_signal(s: SignalIdentifier):
            return self._signal_creator.signal(s.name, s.namespace)

        signals_to_subscribe_on = list(map(to_protobuf_signal, signals_to_subscribe_to))
        wait_for_subscription_queue = queue.Queue()
        Thread(
            target=br.act_on_signal,
            args=(
                client_id,
                self._network_stub,
                signals_to_subscribe_on,
                changed_values_only,  # True: only report when signal changes
                lambda frame: self._on_signals(frame, on_signals),
                lambda sub: (wait_for_subscription_queue.put((self.client_id, sub)))
            ),
        ).start()
        client_id, subscription = wait_for_subscription_queue.get()
        return subscription

    def _on_signals(self, signals_in_frame: network_api.Signals, callback):
        """
        Updates "local" callback or global on_signals callback if local callback is None
        """
        if callback is not None:
            callback(SignalsInFrame(list(map(lambda s: SignalWrapper(s), signals_in_frame))))
        elif self.on_signals is not None:
            self.on_signals(SignalsInFrame(list(map(lambda s: SignalWrapper(s), signals_in_frame))))

    def list_signal_names(self) -> list[SignalIdentifier]:
        # Lists available signals
        configuration = self._system_stub.GetConfiguration(br.common_pb2.Empty())

        signal_names: list[SignalIdentifier] = []
        for networkInfo in configuration.networkInfo:
            res = self._system_stub.ListSignals(networkInfo.namespace)
            for finfo in res.frame:
                # f: br.common_pb2.FrameInfo = finfo
                signal_names.append(SignalIdentifier(finfo.signalInfo.id.name, networkInfo.namespace.name))
                for sinfo in finfo.childInfo:
                    signal_names.append(SignalIdentifier(sinfo.id.name, networkInfo.namespace.name))
        return signal_names
