import uuid
from datetime import datetime

import structlog

from butterrobot.platforms.base import Platform, PlatformMethods
from butterrobot.objects import Message


logger = structlog.get_logger(__name__)


class DebugMethods(PlatformMethods):
    @classmethod
    async def send_message(self, message: Message):
        logger.debug(
            "Outgoing message", message=message.__dict__, platform=DebugPlatform.ID
        )


class DebugPlatform(Platform):
    ID = "debug"

    methods = DebugMethods

    @classmethod
    async def parse_incoming_message(cls, request):
        request_data = await request.get_json()
        logger.debug("Parsing message", data=request_data, platform=cls.ID)

        return Message(
            id=str(uuid.uuid4()),
            date=datetime.now(),
            text=request_data["text"],
            from_bot=bool(request_data.get("from_bot", False)),
            author=request_data.get("author", "Debug author"),
            chat=request_data.get("chat", "Debug chat ID"),
            raw={},
        )
