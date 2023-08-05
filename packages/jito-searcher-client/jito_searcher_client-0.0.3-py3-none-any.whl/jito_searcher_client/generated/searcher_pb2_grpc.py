# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import bundle_pb2 as bundle__pb2
import searcher_pb2 as searcher__pb2


class SearcherServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SubscribeBundleResults = channel.unary_stream(
                '/searcher.SearcherService/SubscribeBundleResults',
                request_serializer=searcher__pb2.SubscribeBundleResultsRequest.SerializeToString,
                response_deserializer=bundle__pb2.BundleResult.FromString,
                )
        self.SubscribePendingTransactions = channel.unary_stream(
                '/searcher.SearcherService/SubscribePendingTransactions',
                request_serializer=searcher__pb2.PendingTxSubscriptionRequest.SerializeToString,
                response_deserializer=searcher__pb2.PendingTxNotification.FromString,
                )
        self.SendBundle = channel.unary_unary(
                '/searcher.SearcherService/SendBundle',
                request_serializer=searcher__pb2.SendBundleRequest.SerializeToString,
                response_deserializer=searcher__pb2.SendBundleResponse.FromString,
                )
        self.GetNextScheduledLeader = channel.unary_unary(
                '/searcher.SearcherService/GetNextScheduledLeader',
                request_serializer=searcher__pb2.NextScheduledLeaderRequest.SerializeToString,
                response_deserializer=searcher__pb2.NextScheduledLeaderResponse.FromString,
                )
        self.GetConnectedLeaders = channel.unary_unary(
                '/searcher.SearcherService/GetConnectedLeaders',
                request_serializer=searcher__pb2.ConnectedLeadersRequest.SerializeToString,
                response_deserializer=searcher__pb2.ConnectedLeadersResponse.FromString,
                )
        self.GetTipAccounts = channel.unary_unary(
                '/searcher.SearcherService/GetTipAccounts',
                request_serializer=searcher__pb2.GetTipAccountsRequest.SerializeToString,
                response_deserializer=searcher__pb2.GetTipAccountsResponse.FromString,
                )


class SearcherServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SubscribeBundleResults(self, request, context):
        """Searchers can invoke this endpoint to subscribe to their respective bundle results.
        A success result would indicate the bundle won its state auction and was submitted to the validator.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribePendingTransactions(self, request, context):
        """RPC endpoint to subscribe to pending transactions. Clients can provide a list of base58 encoded accounts.
        Any transactions that write-lock the provided accounts will be streamed to the searcher.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendBundle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNextScheduledLeader(self, request, context):
        """Returns the next scheduled leader connected to the block engine.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetConnectedLeaders(self, request, context):
        """Returns information on connected leader slots
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTipAccounts(self, request, context):
        """Returns the tip accounts searchers shall transfer funds to for the leader to claim.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SearcherServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SubscribeBundleResults': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeBundleResults,
                    request_deserializer=searcher__pb2.SubscribeBundleResultsRequest.FromString,
                    response_serializer=bundle__pb2.BundleResult.SerializeToString,
            ),
            'SubscribePendingTransactions': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribePendingTransactions,
                    request_deserializer=searcher__pb2.PendingTxSubscriptionRequest.FromString,
                    response_serializer=searcher__pb2.PendingTxNotification.SerializeToString,
            ),
            'SendBundle': grpc.unary_unary_rpc_method_handler(
                    servicer.SendBundle,
                    request_deserializer=searcher__pb2.SendBundleRequest.FromString,
                    response_serializer=searcher__pb2.SendBundleResponse.SerializeToString,
            ),
            'GetNextScheduledLeader': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNextScheduledLeader,
                    request_deserializer=searcher__pb2.NextScheduledLeaderRequest.FromString,
                    response_serializer=searcher__pb2.NextScheduledLeaderResponse.SerializeToString,
            ),
            'GetConnectedLeaders': grpc.unary_unary_rpc_method_handler(
                    servicer.GetConnectedLeaders,
                    request_deserializer=searcher__pb2.ConnectedLeadersRequest.FromString,
                    response_serializer=searcher__pb2.ConnectedLeadersResponse.SerializeToString,
            ),
            'GetTipAccounts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTipAccounts,
                    request_deserializer=searcher__pb2.GetTipAccountsRequest.FromString,
                    response_serializer=searcher__pb2.GetTipAccountsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'searcher.SearcherService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SearcherService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SubscribeBundleResults(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/searcher.SearcherService/SubscribeBundleResults',
            searcher__pb2.SubscribeBundleResultsRequest.SerializeToString,
            bundle__pb2.BundleResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribePendingTransactions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/searcher.SearcherService/SubscribePendingTransactions',
            searcher__pb2.PendingTxSubscriptionRequest.SerializeToString,
            searcher__pb2.PendingTxNotification.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendBundle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/searcher.SearcherService/SendBundle',
            searcher__pb2.SendBundleRequest.SerializeToString,
            searcher__pb2.SendBundleResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNextScheduledLeader(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/searcher.SearcherService/GetNextScheduledLeader',
            searcher__pb2.NextScheduledLeaderRequest.SerializeToString,
            searcher__pb2.NextScheduledLeaderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetConnectedLeaders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/searcher.SearcherService/GetConnectedLeaders',
            searcher__pb2.ConnectedLeadersRequest.SerializeToString,
            searcher__pb2.ConnectedLeadersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTipAccounts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/searcher.SearcherService/GetTipAccounts',
            searcher__pb2.GetTipAccountsRequest.SerializeToString,
            searcher__pb2.GetTipAccountsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
