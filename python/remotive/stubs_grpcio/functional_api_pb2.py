# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: functional_api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x66unctional_api.proto\x12\x04\x62\x61se\x1a\x0c\x63ommon.proto\"]\n\nSenderInfo\x12 \n\x08\x63lientId\x18\x01 \x01(\x0b\x32\x0e.base.ClientId\x12\x1a\n\x05value\x18\x02 \x01(\x0b\x32\x0b.base.Value\x12\x11\n\tfrequency\x18\x03 \x01(\x05\"G\n\x11SubscriberRequest\x12 \n\x08\x63lientId\x18\x01 \x01(\x0b\x32\x0e.base.ClientId\x12\x10\n\x08onChange\x18\x02 \x01(\x08\"\x18\n\x05Value\x12\x0f\n\x07payload\x18\x01 \x01(\x05\x32\xe7\x01\n\x11\x46unctionalService\x12/\n\x0eOpenPassWindow\x12\x0e.base.ClientId\x1a\x0b.base.Empty\"\x00\x12\x30\n\x0f\x43losePassWindow\x12\x0e.base.ClientId\x1a\x0b.base.Empty\"\x00\x12.\n\x0bSetFanSpeed\x12\x10.base.SenderInfo\x1a\x0b.base.Empty\"\x00\x12?\n\x13SubscribeToFanSpeed\x12\x17.base.SubscriberRequest\x1a\x0b.base.Value\"\x00\x30\x01\x62\x06proto3')



_SENDERINFO = DESCRIPTOR.message_types_by_name['SenderInfo']
_SUBSCRIBERREQUEST = DESCRIPTOR.message_types_by_name['SubscriberRequest']
_VALUE = DESCRIPTOR.message_types_by_name['Value']
SenderInfo = _reflection.GeneratedProtocolMessageType('SenderInfo', (_message.Message,), {
  'DESCRIPTOR' : _SENDERINFO,
  '__module__' : 'functional_api_pb2'
  # @@protoc_insertion_point(class_scope:base.SenderInfo)
  })
_sym_db.RegisterMessage(SenderInfo)

SubscriberRequest = _reflection.GeneratedProtocolMessageType('SubscriberRequest', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBERREQUEST,
  '__module__' : 'functional_api_pb2'
  # @@protoc_insertion_point(class_scope:base.SubscriberRequest)
  })
_sym_db.RegisterMessage(SubscriberRequest)

Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), {
  'DESCRIPTOR' : _VALUE,
  '__module__' : 'functional_api_pb2'
  # @@protoc_insertion_point(class_scope:base.Value)
  })
_sym_db.RegisterMessage(Value)

_FUNCTIONALSERVICE = DESCRIPTOR.services_by_name['FunctionalService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SENDERINFO._serialized_start=44
  _SENDERINFO._serialized_end=137
  _SUBSCRIBERREQUEST._serialized_start=139
  _SUBSCRIBERREQUEST._serialized_end=210
  _VALUE._serialized_start=212
  _VALUE._serialized_end=236
  _FUNCTIONALSERVICE._serialized_start=239
  _FUNCTIONALSERVICE._serialized_end=470
# @@protoc_insertion_point(module_scope)
