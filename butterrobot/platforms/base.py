from abc import abstractmethod
from dataclasses import dataclass


class Platform:
    class PlatformError(Exception):
        pass

    class PlatformInitError(PlatformError):
        pass

    class PlatformAuthError(PlatformError):
        pass

    @dataclass
    class PlatformAuthResponse(PlatformError):
        """
        Used when the platform needs to make a response right away instead of async.
        """

        data: dict
        status_code: int = 200

    @classmethod
    def init(cls, app):
        """
        Initialises the platform.

        Used at the application launch to prepare anything required for
        the platform to work..

        It receives the flask application via parameter in case the platform
        requires for custom webservice endpoints or configuration.
        """
        pass

    @classmethod
    @abstractmethod
    def parse_incoming_message(cls, request) -> 'Message':
        """
        Parses the incoming request and returns a :class:`butterrobot.objects.Message` instance.
        """
        pass

    @classmethod
    @abstractmethod
    def parse_channel_name_from_raw(cls, channel_raw) -> str:
        """
        Extracts the Channel name from :class:`butterrobot.objects.Channel.channel_raw`.
        """
        pass

    @classmethod
    @abstractmethod
    def parse_channel_from_message(cls, channel_raw) -> 'Channel':
        """
        Extracts the Channel raw data from the message received in the incoming webhook.
        """
        pass


class PlatformMethods:
    @classmethod
    @abstractmethod
    def send_message(cls, message: 'Message'):
        """Method used to send a message via the platform"""
        pass
