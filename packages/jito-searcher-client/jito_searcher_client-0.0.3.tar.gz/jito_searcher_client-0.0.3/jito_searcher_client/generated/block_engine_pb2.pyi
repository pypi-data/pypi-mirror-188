"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import bundle_pb2
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import packet_pb2
import shared_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class SubscribePacketsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___SubscribePacketsRequest = SubscribePacketsRequest

@typing_extensions.final
class SubscribePacketsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEADER_FIELD_NUMBER: builtins.int
    BATCH_FIELD_NUMBER: builtins.int
    @property
    def header(self) -> shared_pb2.Header: ...
    @property
    def batch(self) -> packet_pb2.PacketBatch: ...
    def __init__(
        self,
        *,
        header: shared_pb2.Header | None = ...,
        batch: packet_pb2.PacketBatch | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["batch", b"batch", "header", b"header"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["batch", b"batch", "header", b"header"]) -> None: ...

global___SubscribePacketsResponse = SubscribePacketsResponse

@typing_extensions.final
class SubscribeBundlesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___SubscribeBundlesRequest = SubscribeBundlesRequest

@typing_extensions.final
class SubscribeBundlesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BUNDLES_FIELD_NUMBER: builtins.int
    @property
    def bundles(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[bundle_pb2.BundleUuid]: ...
    def __init__(
        self,
        *,
        bundles: collections.abc.Iterable[bundle_pb2.BundleUuid] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["bundles", b"bundles"]) -> None: ...

global___SubscribeBundlesResponse = SubscribeBundlesResponse

@typing_extensions.final
class BlockBuilderFeeInfoRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___BlockBuilderFeeInfoRequest = BlockBuilderFeeInfoRequest

@typing_extensions.final
class BlockBuilderFeeInfoResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PUBKEY_FIELD_NUMBER: builtins.int
    COMMISSION_FIELD_NUMBER: builtins.int
    pubkey: builtins.str
    commission: builtins.int
    """commission (0-100)"""
    def __init__(
        self,
        *,
        pubkey: builtins.str = ...,
        commission: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["commission", b"commission", "pubkey", b"pubkey"]) -> None: ...

global___BlockBuilderFeeInfoResponse = BlockBuilderFeeInfoResponse

@typing_extensions.final
class AccountsOfInterest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCOUNTS_FIELD_NUMBER: builtins.int
    @property
    def accounts(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """use * for all accounts"""
    def __init__(
        self,
        *,
        accounts: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["accounts", b"accounts"]) -> None: ...

global___AccountsOfInterest = AccountsOfInterest

@typing_extensions.final
class AccountsOfInterestRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___AccountsOfInterestRequest = AccountsOfInterestRequest

@typing_extensions.final
class AccountsOfInterestUpdate(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADD_FIELD_NUMBER: builtins.int
    REMOVE_FIELD_NUMBER: builtins.int
    OVERWRITE_FIELD_NUMBER: builtins.int
    @property
    def add(self) -> global___AccountsOfInterest: ...
    @property
    def remove(self) -> global___AccountsOfInterest: ...
    @property
    def overwrite(self) -> global___AccountsOfInterest: ...
    def __init__(
        self,
        *,
        add: global___AccountsOfInterest | None = ...,
        remove: global___AccountsOfInterest | None = ...,
        overwrite: global___AccountsOfInterest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["add", b"add", "msg", b"msg", "overwrite", b"overwrite", "remove", b"remove"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["add", b"add", "msg", b"msg", "overwrite", b"overwrite", "remove", b"remove"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["msg", b"msg"]) -> typing_extensions.Literal["add", "remove", "overwrite"] | None: ...

global___AccountsOfInterestUpdate = AccountsOfInterestUpdate

@typing_extensions.final
class ExpiringPacketBatch(google.protobuf.message.Message):
    """A series of packets with an expiration attached to them.
    The header contains a timestamp for when this packet was generated.
    The expiry is how long the packet batches have before they expire and are forwarded to the validator.
    This provides a more censorship resistant method to MEV than block engines receiving packets directly.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEADER_FIELD_NUMBER: builtins.int
    BATCH_FIELD_NUMBER: builtins.int
    EXPIRY_MS_FIELD_NUMBER: builtins.int
    @property
    def header(self) -> shared_pb2.Header: ...
    @property
    def batch(self) -> packet_pb2.PacketBatch: ...
    expiry_ms: builtins.int
    def __init__(
        self,
        *,
        header: shared_pb2.Header | None = ...,
        batch: packet_pb2.PacketBatch | None = ...,
        expiry_ms: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["batch", b"batch", "header", b"header"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["batch", b"batch", "expiry_ms", b"expiry_ms", "header", b"header"]) -> None: ...

global___ExpiringPacketBatch = ExpiringPacketBatch

@typing_extensions.final
class PacketBatchUpdate(google.protobuf.message.Message):
    """Packets and heartbeats are sent over the same stream.
    ExpiringPacketBatches have an expiration attached to them so the block engine can track
    how long it has until the relayer forwards the packets to the validator.
    Heartbeats contain a timestamp from the system and is used as a simple and naive time-sync mechanism
    so the block engine has some idea on how far their clocks are apart.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BATCHES_FIELD_NUMBER: builtins.int
    HEARTBEAT_FIELD_NUMBER: builtins.int
    @property
    def batches(self) -> global___ExpiringPacketBatch: ...
    @property
    def heartbeat(self) -> shared_pb2.Heartbeat: ...
    def __init__(
        self,
        *,
        batches: global___ExpiringPacketBatch | None = ...,
        heartbeat: shared_pb2.Heartbeat | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["batches", b"batches", "heartbeat", b"heartbeat", "msg", b"msg"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["batches", b"batches", "heartbeat", b"heartbeat", "msg", b"msg"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["msg", b"msg"]) -> typing_extensions.Literal["batches", "heartbeat"] | None: ...

global___PacketBatchUpdate = PacketBatchUpdate

@typing_extensions.final
class StartExpiringPacketStreamResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEARTBEAT_FIELD_NUMBER: builtins.int
    @property
    def heartbeat(self) -> shared_pb2.Heartbeat: ...
    def __init__(
        self,
        *,
        heartbeat: shared_pb2.Heartbeat | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["heartbeat", b"heartbeat"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["heartbeat", b"heartbeat"]) -> None: ...

global___StartExpiringPacketStreamResponse = StartExpiringPacketStreamResponse
