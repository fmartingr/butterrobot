from abc import abstractclassmethod
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
    async def init(cls, app):
        pass


class PlatformMethods:
    @abstractclassmethod
    def send_message(cls, message):
        pass

    @abstractclassmethod
    def reply_message(cls, message, reply_to):
        pass
