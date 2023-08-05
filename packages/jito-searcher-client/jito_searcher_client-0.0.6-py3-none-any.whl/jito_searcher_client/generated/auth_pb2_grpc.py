# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import auth_pb2 as auth__pb2


class AuthServiceStub(object):
    """/ This service is responsible for issuing auth tokens to clients for API access.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GenerateAuthChallenge = channel.unary_unary(
                '/auth.AuthService/GenerateAuthChallenge',
                request_serializer=auth__pb2.GenerateAuthChallengeRequest.SerializeToString,
                response_deserializer=auth__pb2.GenerateAuthChallengeResponse.FromString,
                )
        self.GenerateAuthTokens = channel.unary_unary(
                '/auth.AuthService/GenerateAuthTokens',
                request_serializer=auth__pb2.GenerateAuthTokensRequest.SerializeToString,
                response_deserializer=auth__pb2.GenerateAuthTokensResponse.FromString,
                )
        self.RefreshAccessToken = channel.unary_unary(
                '/auth.AuthService/RefreshAccessToken',
                request_serializer=auth__pb2.RefreshAccessTokenRequest.SerializeToString,
                response_deserializer=auth__pb2.RefreshAccessTokenResponse.FromString,
                )


class AuthServiceServicer(object):
    """/ This service is responsible for issuing auth tokens to clients for API access.
    """

    def GenerateAuthChallenge(self, request, context):
        """/ Returns a challenge, client is expected to sign this challenge with an appropriate keypair in order to obtain access tokens.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GenerateAuthTokens(self, request, context):
        """/ Provides the client with the initial pair of auth tokens for API access.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RefreshAccessToken(self, request, context):
        """/ Call this method with a non-expired refresh token to obtain a new access token.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GenerateAuthChallenge': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateAuthChallenge,
                    request_deserializer=auth__pb2.GenerateAuthChallengeRequest.FromString,
                    response_serializer=auth__pb2.GenerateAuthChallengeResponse.SerializeToString,
            ),
            'GenerateAuthTokens': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateAuthTokens,
                    request_deserializer=auth__pb2.GenerateAuthTokensRequest.FromString,
                    response_serializer=auth__pb2.GenerateAuthTokensResponse.SerializeToString,
            ),
            'RefreshAccessToken': grpc.unary_unary_rpc_method_handler(
                    servicer.RefreshAccessToken,
                    request_deserializer=auth__pb2.RefreshAccessTokenRequest.FromString,
                    response_serializer=auth__pb2.RefreshAccessTokenResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'auth.AuthService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AuthService(object):
    """/ This service is responsible for issuing auth tokens to clients for API access.
    """

    @staticmethod
    def GenerateAuthChallenge(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/auth.AuthService/GenerateAuthChallenge',
            auth__pb2.GenerateAuthChallengeRequest.SerializeToString,
            auth__pb2.GenerateAuthChallengeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GenerateAuthTokens(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/auth.AuthService/GenerateAuthTokens',
            auth__pb2.GenerateAuthTokensRequest.SerializeToString,
            auth__pb2.GenerateAuthTokensResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RefreshAccessToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/auth.AuthService/RefreshAccessToken',
            auth__pb2.RefreshAccessTokenRequest.SerializeToString,
            auth__pb2.RefreshAccessTokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
