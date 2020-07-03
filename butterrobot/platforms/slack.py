from datetime import datetime

import structlog

from butterrobot.platforms.base import Platform, PlatformMethods
from butterrobot.config import SLACK_TOKEN, SLACK_BOT_OAUTH_ACCESS_TOKEN
from butterrobot.objects import Message
from butterrobot.lib.slack import SlackAPI


logger = structlog.get_logger(__name__)


class SlackMethods(PlatformMethods):
    @classmethod
    async def send_message(self, message: Message):
        logger.debug(
            "Outgoing message", message=message.__dict__, platform=SlackPlatform.ID
        )
        try:
            await SlackAPI.send_message(
                channel=message.chat, message=message.text, thread=message.reply_to
            )
        except SlackAPI.SlackClientError as error:
            logger.error(
                "Send message error",
                platform=SlackPlatform.ID,
                error=error,
                message=message.__dict__,
            )


class SlackPlatform(Platform):
    ID = "slack"

    methods = SlackMethods

    @classmethod
    async def init(cls, app):
        if not (SLACK_TOKEN and SLACK_BOT_OAUTH_ACCESS_TOKEN):
            logger.error("Missing token. platform not enabled.", platform=cls.ID)
            return

    @classmethod
    async def parse_incoming_message(cls, request):
        data = await request.get_json()
        logger.debug("Parsing message", platform=cls.ID, data=data)

        # Auth
        if data.get("token") != SLACK_TOKEN:
            raise cls.PlatformAuthError("Authentication error")

        # Confirms challenge request to configure webhook
        if "challenge" in data:
            raise cls.PlatformAuthResponse(data={"challenge": data["challenge"]})

        # Discard messages by bots
        if "bot_id" in data["event"]:
            return

        if data["event"]["type"] != "message":
            return

        return Message(
            id=data["event"].get("thread_ts", data["event"]["ts"]),
            date=datetime.fromtimestamp(int(float(data["event"]["event_ts"]))),
            text=data["event"]["text"],
            chat=data["event"]["channel"],
            raw=data,
        )
