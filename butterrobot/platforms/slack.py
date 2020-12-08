from datetime import datetime

import structlog

from butterrobot.platforms.base import Platform, PlatformMethods
from butterrobot.config import SLACK_TOKEN, SLACK_BOT_OAUTH_ACCESS_TOKEN
from butterrobot.objects import Message, Channel
from butterrobot.lib.slack import SlackAPI


logger = structlog.get_logger(__name__)


class SlackMethods(PlatformMethods):
    @classmethod
    def send_message(self, message: Message):
        logger.debug(
            "Outgoing message", message=message.__dict__, platform=SlackPlatform.ID
        )
        try:
            SlackAPI.send_message(
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
    def init(cls, app):
        if not (SLACK_TOKEN and SLACK_BOT_OAUTH_ACCESS_TOKEN):
            logger.error("Missing token. platform not enabled.", platform=cls.ID)
            return

    @classmethod
    def parse_channel_name_from_raw(cls, channel_raw):
        return channel_raw["name"]

    @classmethod
    def parse_channel_from_message(cls, message):
        # Call different APIs for a channel or DM
        if message["event"]["channel_type"] == "im":
            chat_raw = SlackAPI.get_user_info(message["event"]["user"])
        else:
            chat_raw = SlackAPI.get_conversations_info(message["event"]["channel"])

        return Channel(
            platform=cls.ID,
            platform_channel_id=message["event"]["channel"],
            channel_raw=chat_raw,
        )

    @classmethod
    def parse_incoming_message(cls, request):
        data = request["json"]

        # Auth
        if data.get("token") != SLACK_TOKEN:
            raise cls.PlatformAuthError("Authentication error")

        # Confirms challenge request to configure webhook
        if "challenge" in data:
            raise cls.PlatformAuthResponse(data={"challenge": data["challenge"]})

        # Discard messages by webhooks and apps
        if "bot_id" in data["event"]:
            logger.debug("Discarding message", data=data)
            return

        if data["event"]["type"] != "message":
            return

        logger.debug("Parsing message", platform=cls.ID, data=data)
        return Message(
            id=data["event"].get("thread_ts", data["event"]["ts"]),
            author=data["event"]["user"],
            from_bot="bot_id" in data["event"],
            date=datetime.fromtimestamp(int(float(data["event"]["event_ts"]))),
            text=data["event"]["text"],
            chat=data["event"]["channel"],
            channel=cls.parse_channel_from_message(data),
            raw=data,
        )
