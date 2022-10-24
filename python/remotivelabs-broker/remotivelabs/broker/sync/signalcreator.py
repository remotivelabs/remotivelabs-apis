import sys

import logging

from ..generated.sync import common_pb2
from ..generated.sync import network_api_pb2

from typing import Optional, TypeVar, Sequence

T = TypeVar("T")

_logger = logging.getLogger("remotivelabs.SignalCreator")
_MSG_DUPLICATE = (
    "Warning duplicated (namespace.signal): {}, to avoid"
    + 'ambiguity set "short_names": false in your interfaces.json on {}'
)


class MetaGetter:
    def __init__(self, proto_message):
        self.meta = proto_message

    def _getDefault(field: T, default: Optional[T]) -> T:
        if field is not None:
            return field
        elif default:
            return default
        else:
            raise Exception("Failed to retrieve meta data field")

    def getDescription(self, default: Optional[str] = None) -> str:
        """Get protobuffer MetaData field description"""
        return MetaGetter._getDefault(self.meta.description, default)

    def getUnit(self, default: Optional[str] = None) -> str:
        """Get protobuffer MetaData field unit"""
        return MetaGetter._getDefault(self.meta.unit, default)

    def getMax(self, default: Optional[float] = None) -> float:
        """Get protobuffer MetaData field max"""
        return MetaGetter._getDefault(self.meta.max, default)

    def getMin(self, default: Optional[float] = None) -> float:
        """Get protobuffer MetaData field min"""
        return MetaGetter._getDefault(self.meta.min, default)

    def getSize(self, default: Optional[int] = None) -> int:
        """Get protobuffer MetaData field size"""
        return MetaGetter._getDefault(self.meta.size, default)

    def getIsRaw(self, default: Optional[bool] = None) -> bool:
        """Get protobuffer MetaData field isRaw"""
        return MetaGetter._getDefault(self.meta.isRaw, default)

    def getFactor(self, default: Optional[float] = None) -> float:
        """Get protobuffer MetaData field factor"""
        return MetaGetter._getDefault(self.meta.factor, default)

    def getOffset(self, default: Optional[float] = None) -> float:
        """Get protobuffer MetaData field offset"""
        return MetaGetter._getDefault(self.meta.offset, default)

    def getSenders(
            self, default: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        """Get protobuffer MetaData field sender"""
        return MetaGetter._getDefault(self.meta.sender, default)

    def getReceivers(
            self, default: Optional[Sequence[str]] = None
    ) -> Sequence[str]:
        """Get protobuffer MetaData field receiver"""
        return MetaGetter._getDefault(self.meta.receiver, default)

    def getCycleTime(self, default: Optional[float] = None) -> float:
        """Get protobuffer MetaData field cycleTime"""
        return MetaGetter._getDefault(self.meta.cycleTime, default)

    def getStartValue(self, default: Optional[float] = None) -> float:
        """Get protobuffer MetaData field startValue"""
        return MetaGetter._getDefault(self.meta.startValue, default)


class SignalCreator:
    """
    Class for prepearing and writing signals via gRPC.
    """

    def __init__(self, system_stub):
        self._sinfos = {}
        self._virtual = []
        self._networks = {}
        namespaces = []
        conf = system_stub.GetConfiguration(common_pb2.Empty())
        for ninfo in conf.networkInfo:
            namespaces.append(ninfo.namespace)
            if ninfo.type == "virtual":
                self._virtual.append(ninfo.namespace.name)
        for namespace in namespaces:
            res = system_stub.ListSignals(namespace)
            self._addframes(namespace, res)
            for finfo in res.frame:
                self._add(finfo.signalInfo)
                for sinfo in finfo.childInfo:
                    self._add(sinfo)

    def _addframes(self, namespace, res):
        self._networks[namespace.name] = res

    def _add(self, sinfo):
        k = (sinfo.id.namespace.name, sinfo.id.name)
        if k in self._sinfos:
            msg = _MSG_DUPLICATE.format(k, sinfo.id.namespace)
            _logger.warning(msg)
        self._sinfos[k] = MetaGetter(sinfo.metaData)

    def get_meta(self, name: str, namespace_name: str) -> MetaGetter:
        """
        Get meta fields for signal or frame

        :param name: Name of signal or frame
        :param namespace_name: Namespace for given signal or frame
        """

        k = (namespace_name, name)
        if (k not in self._sinfos) and (namespace_name not in self._virtual):
            raise Exception(f"signal not declared (namespace, signal): {k}")
        return self._sinfos[k]

    def signal(self, name: str, namespace_name: str) -> common_pb2.SignalId:
        """
        Create object for signal.

        :param name: Name of signal
        :param namespace_name: Namespace for signal
        """

        self.get_meta(name, namespace_name)  # Checks if the signal is present
        return common_pb2.SignalId(
            name=name, namespace=common_pb2.NameSpace(name=namespace_name)
        )

    def frames(self, namespace_name: str) -> Sequence[common_pb2.SignalId]:
        """
        Get all frames in given namespace
        """

        all_frames = []
        for finfo in self._networks[namespace_name].frame:
            all_frames.append(self.signal(finfo.signalInfo.id.name,
                                          namespace_name))
        return all_frames

    def frame_by_signal(
        self, name: str, namespace_name: str
    ) -> Sequence[common_pb2.SignalId]:
        """
        Get frame for the given signal.

        :param name: Name of signal
        :param namespace_name: Name of namespace
        :return: Protobuffer type for Signal
        """

        for finfo in self._networks[namespace_name].frame:
            for sinfo in finfo.childInfo:
                if sinfo.id.name == name:
                    return self.signal(finfo.signalInfo.id.name,
                                       namespace_name)
        raise Exception(
            f"signal not declared (namespace, signal): {namespace_name} {name}"
        )

    def signals_in_frame(
        self, name: str, namespace_name: str
    ) -> Sequence[common_pb2.SignalId]:
        """
        Get all signals residing in the frame.

        :param name: Name of frame
        :param namespace_name: Namespace for frame
        :rtype: [common_pb2.SignalId]
        """

        all_signals = []
        frame = None
        for finfo in self._networks[namespace_name].frame:
            if finfo.signalInfo.id.name == name:
                frame = finfo
                for sinfo in finfo.childInfo:
                    all_signals.append(self.signal(sinfo.id.name,
                                                   namespace_name))
        assert (
            frame is not None
        ), f"frame {name} does not exist in namespace {namespace_name}"
        return all_signals

    def signal_with_payload(
        self, name: str, namespace_name: str, value_pair,
        allow_malformed: bool = False
    ) -> network_api_pb2.Signal:
        """
        Create value with signal for writing.

        :param name: Name of frame
        :param namespace_name: Namespace for frame
        :return: Signal with value
        :rtype: network_api_pb2.Signal
        """

        signal = self.signal(name, namespace_name)
        meta = self.get_meta(name, namespace_name)

        key, value = value_pair
        types = ["integer", "double", "raw", "arbitration"]
        if key not in types:
            raise Exception(f"type must be one of: {types}")
        if key == "raw" and allow_malformed is False:
            expected = meta.getSize()
            assert (
                len(value) * 8 == expected
            ), f"payload size missmatch, expected {expected/8} bytes"
        elif key != "raw":
            # Check bounds if any
            checkMin = meta.getMin()
            if (checkMin is not None) and (value < checkMin):
                _logger.warning(
                    'Value below minimum value of {} for signal "{}"'.format(
                        checkMin, name
                    )
                )
            checkMax = meta.getMax()
            if (checkMax is not None) and (value > checkMax):
                _logger.warning(
                    'Value above maximum value of {} for signal "{}"'.format(
                        checkMax, name
                    )
                )

        params = {"id": signal, key: value}
        return network_api_pb2.Signal(**params)

        # Above is simlar as this, but parameterised.
        # return network_api_pb2.Signal(
        #     id=signal, value_dict.get_key=value_dict["integer"]
        # )
