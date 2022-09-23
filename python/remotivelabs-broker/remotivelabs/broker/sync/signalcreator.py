import sys

from ..stubs_grpcio import common_pb2
from ..stubs_grpcio import network_api_pb2

class MetaGetter:
    def __init__(self, proto_message):
        self.meta = proto_message

    def _getDefault(field, default):
        if field != None:
            return field
        elif default:
            return default
        else:
            raise Exception("Failed to retrieve meta data field")

    def getDescription(self, default=None):
        return MetaGetter._getDefault(self.meta.description, default)

    def getUnit(self, default=None):
        return MetaGetter._getDefault(self.meta.unit, default)

    def getMax(self, default=None):
        return MetaGetter._getDefault(self.meta.max, default)

    def getMin(self, default=None):
        return MetaGetter._getDefault(self.meta.min, default)

    def getSize(self, default=None):
        return MetaGetter._getDefault(self.meta.size, default)

    def getIsRaw(self, default=None):
        return MetaGetter._getDefault(self.meta.isRaw, default)

    def getFactor(self, default=None):
        return MetaGetter._getDefault(self.meta.factor, default)

    def getOffset(self, default=None):
        return MetaGetter._getDefault(self.meta.offset, default)

    def getSenders(self, default=None):
        return MetaGetter._getDefault(self.meta.sender, default)

    def getReceivers(self, default=None):
        return MetaGetter._getDefault(self.meta.receiver, default)

    def getCycleTime(self, default=None):
        return MetaGetter._getDefault(self.meta.cycleTime, default)

    def getStartValue(self, default=None):
        return MetaGetter._getDefault(self.meta.startValue, default)

class SignalCreator:
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
            raise Exception(f"duplicate (namespace,signal): {k}")
        self._sinfos[k] = MetaGetter(sinfo.metaData)

    def get_meta(self, name, namespace_name):
        k = (namespace_name, name)
        if (k not in self._sinfos) and (namespace_name not in self._virtual):
            raise Exception(f"signal not declared (namespace, signal): {k}")
        return self._sinfos[k]

    def signal(self, name, namespace_name):
        self.get_meta(name, namespace_name) # Checks if the signal is present
        return common_pb2.SignalId(
            name=name, namespace=common_pb2.NameSpace(name=namespace_name)
        )

    def frames(self, namespace_name):
        all_frames = []
        for finfo in self._networks[namespace_name].frame:
            all_frames.append(self.signal(finfo.signalInfo.id.name, namespace_name))
            # all_frames.append(finfo) 
        return all_frames

    def frame_by_signal(self, name, namespace_name):
        for finfo in self._networks[namespace_name].frame:
            for sinfo in finfo.childInfo:
                if sinfo.id.name == name:
                    return self.signal(finfo.signalInfo.id.name, namespace_name)
        raise Exception(f"signal not declared (namespace, signal): {namespace_name} {name}")

    def signals_in_frame(self, name, namespace_name):
        all_signals = []
        frame = None
        for finfo in self._networks[namespace_name].frame:
            if finfo.signalInfo.id.name == name:
                frame = finfo
                for sinfo in finfo.childInfo:
                    all_signals.append(self.signal(sinfo.id.name, namespace_name))
        assert frame != None, f"frame {name} does not exist in namespace {namespace_name}"
        return all_signals

    def signal_with_payload(self, name, namespace_name, value_pair, allow_malformed = False):
        signal = self.signal(name, namespace_name)

        key, value = value_pair
        types = ["integer", "double", "raw", "arbitration"]
        if key not in types:
            raise Exception(f"type must be one of: {types}")
        if key == "raw" and allow_malformed == False:
            expeceted = self.get_meta(namespace_name, name).getSize()
            assert len(value)*8 == expected, f"payload size missmatch, expected {expected/8} bytes"
        params = {"id": signal, key: value}
        return network_api_pb2.Signal(**params)

        # Above is simlar as this, but parameterised.
        # return network_api_pb2.Signal(
        #     id=signal, value_dict.get_key=value_dict["integer"]
        # )
