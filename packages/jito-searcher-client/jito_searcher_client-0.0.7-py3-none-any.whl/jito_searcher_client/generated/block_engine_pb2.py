# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: block_engine.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import packet_pb2 as packet__pb2
import shared_pb2 as shared__pb2
import bundle_pb2 as bundle__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x62lock_engine.proto\x12\x0c\x62lock_engine\x1a\x0cpacket.proto\x1a\x0cshared.proto\x1a\x0c\x62undle.proto\"\x19\n\x17SubscribePacketsRequest\"^\n\x18SubscribePacketsResponse\x12\x1e\n\x06header\x18\x01 \x01(\x0b\x32\x0e.shared.Header\x12\"\n\x05\x62\x61tch\x18\x02 \x01(\x0b\x32\x13.packet.PacketBatch\"\x19\n\x17SubscribeBundlesRequest\"?\n\x18SubscribeBundlesResponse\x12#\n\x07\x62undles\x18\x01 \x03(\x0b\x32\x12.bundle.BundleUuid\"\x1c\n\x1a\x42lockBuilderFeeInfoRequest\"A\n\x1b\x42lockBuilderFeeInfoResponse\x12\x0e\n\x06pubkey\x18\x01 \x01(\t\x12\x12\n\ncommission\x18\x02 \x01(\x04\"&\n\x12\x41\x63\x63ountsOfInterest\x12\x10\n\x08\x61\x63\x63ounts\x18\x01 \x03(\t\"\x1b\n\x19\x41\x63\x63ountsOfInterestRequest\"\xbd\x01\n\x18\x41\x63\x63ountsOfInterestUpdate\x12/\n\x03\x61\x64\x64\x18\x01 \x01(\x0b\x32 .block_engine.AccountsOfInterestH\x00\x12\x32\n\x06remove\x18\x02 \x01(\x0b\x32 .block_engine.AccountsOfInterestH\x00\x12\x35\n\toverwrite\x18\x03 \x01(\x0b\x32 .block_engine.AccountsOfInterestH\x00\x42\x05\n\x03msg\"l\n\x13\x45xpiringPacketBatch\x12\x1e\n\x06header\x18\x01 \x01(\x0b\x32\x0e.shared.Header\x12\"\n\x05\x62\x61tch\x18\x02 \x01(\x0b\x32\x13.packet.PacketBatch\x12\x11\n\texpiry_ms\x18\x03 \x01(\r\"x\n\x11PacketBatchUpdate\x12\x34\n\x07\x62\x61tches\x18\x01 \x01(\x0b\x32!.block_engine.ExpiringPacketBatchH\x00\x12&\n\theartbeat\x18\x02 \x01(\x0b\x32\x11.shared.HeartbeatH\x00\x42\x05\n\x03msg\"I\n!StartExpiringPacketStreamResponse\x12$\n\theartbeat\x18\x01 \x01(\x0b\x32\x11.shared.Heartbeat2\xd5\x02\n\x14\x42lockEngineValidator\x12\x65\n\x10SubscribePackets\x12%.block_engine.SubscribePacketsRequest\x1a&.block_engine.SubscribePacketsResponse\"\x00\x30\x01\x12\x65\n\x10SubscribeBundles\x12%.block_engine.SubscribeBundlesRequest\x1a&.block_engine.SubscribeBundlesResponse\"\x00\x30\x01\x12o\n\x16GetBlockBuilderFeeInfo\x12(.block_engine.BlockBuilderFeeInfoRequest\x1a).block_engine.BlockBuilderFeeInfoResponse\"\x00\x32\xfd\x01\n\x12\x42lockEngineRelayer\x12r\n\x1bSubscribeAccountsOfInterest\x12\'.block_engine.AccountsOfInterestRequest\x1a&.block_engine.AccountsOfInterestUpdate\"\x00\x30\x01\x12s\n\x19StartExpiringPacketStream\x12\x1f.block_engine.PacketBatchUpdate\x1a/.block_engine.StartExpiringPacketStreamResponse\"\x00(\x01\x30\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'block_engine_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SUBSCRIBEPACKETSREQUEST._serialized_start=78
  _SUBSCRIBEPACKETSREQUEST._serialized_end=103
  _SUBSCRIBEPACKETSRESPONSE._serialized_start=105
  _SUBSCRIBEPACKETSRESPONSE._serialized_end=199
  _SUBSCRIBEBUNDLESREQUEST._serialized_start=201
  _SUBSCRIBEBUNDLESREQUEST._serialized_end=226
  _SUBSCRIBEBUNDLESRESPONSE._serialized_start=228
  _SUBSCRIBEBUNDLESRESPONSE._serialized_end=291
  _BLOCKBUILDERFEEINFOREQUEST._serialized_start=293
  _BLOCKBUILDERFEEINFOREQUEST._serialized_end=321
  _BLOCKBUILDERFEEINFORESPONSE._serialized_start=323
  _BLOCKBUILDERFEEINFORESPONSE._serialized_end=388
  _ACCOUNTSOFINTEREST._serialized_start=390
  _ACCOUNTSOFINTEREST._serialized_end=428
  _ACCOUNTSOFINTERESTREQUEST._serialized_start=430
  _ACCOUNTSOFINTERESTREQUEST._serialized_end=457
  _ACCOUNTSOFINTERESTUPDATE._serialized_start=460
  _ACCOUNTSOFINTERESTUPDATE._serialized_end=649
  _EXPIRINGPACKETBATCH._serialized_start=651
  _EXPIRINGPACKETBATCH._serialized_end=759
  _PACKETBATCHUPDATE._serialized_start=761
  _PACKETBATCHUPDATE._serialized_end=881
  _STARTEXPIRINGPACKETSTREAMRESPONSE._serialized_start=883
  _STARTEXPIRINGPACKETSTREAMRESPONSE._serialized_end=956
  _BLOCKENGINEVALIDATOR._serialized_start=959
  _BLOCKENGINEVALIDATOR._serialized_end=1300
  _BLOCKENGINERELAYER._serialized_start=1303
  _BLOCKENGINERELAYER._serialized_end=1556
# @@protoc_insertion_point(module_scope)
