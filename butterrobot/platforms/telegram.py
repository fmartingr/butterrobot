from datetime import datetime

import structlog

from butterrobot.platforms.base import Platform, PlatformMethods
from butterrobot.config import TELEGRAM_TOKEN, HOSTNAME
from butterrobot.lib.telegram import TelegramAPI
from butterrobot.objects import Message, Channel


logger = structlog.get_logger(__name__)


class TelegramMethods(PlatformMethods):
    @classmethod
    def send_message(self, message: Message):
        logger.debug(
            "Outgoing message", message=message.__dict__, platform=TelegramPlatform.ID
        )
        TelegramAPI.send_message(
            chat_id=message.chat,
            text=message.text,
            reply_to_message_id=message.reply_to,
        )


class TelegramPlatform(Platform):
    ID = "telegram"

    methods = TelegramMethods

    @classmethod
    def init(cls, app):
        """
        Initializes the Telegram webhook endpoint to receive updates
        """

        if not TELEGRAM_TOKEN:
            logger.error("Missing token. platform not enabled.", platform=cls.ID)
            return

        webhook_url = f"https://{HOSTNAME}/telegram/incoming/{TELEGRAM_TOKEN}"
        try:
            TelegramAPI.set_webhook(webhook_url)
        except TelegramAPI.TelegramError as error:
            logger.error(f"Error setting Telegram webhook: {error}", platform=cls.ID)
            raise Platform.PlatformInitError()

    @classmethod
    def parse_channel_name_from_raw(cls, channel_raw):
        if channel_raw["id"] < 0:
            return channel_raw["title"]
        else:
            if channel_raw["username"]:
                return f"@{channel_raw['username']}"
        return f"{channel_raw['first_name']} {channel_raw['last_name']}"

    @classmethod
    def parse_channel_from_message(cls, channel_raw):
        return Channel(
            platform=cls.ID,
            platform_channel_id=channel_raw["id"],
            channel_raw=channel_raw,
        )

    @classmethod
    def parse_incoming_message(cls, request):
        token = request["path"].split("/")[-1]
        if token != TELEGRAM_TOKEN:
            raise cls.PlatformAuthError("Authentication error")

        logger.debug("Parsing message", data=request["json"], platform=cls.ID)

        if "text" in request["json"]["message"]:
            # Ignore all messages but text messages
            return Message(
                id=request["json"]["message"]["message_id"],
                date=datetime.fromtimestamp(request["json"]["message"]["date"]),
                text=str(request["json"]["message"]["text"]),
                from_bot=request["json"]["message"]["from"]["is_bot"],
                author=request["json"]["message"]["from"]["id"],
                chat=str(request["json"]["message"]["chat"]["id"]),
                channel=cls.parse_channel_from_message(
                    request["json"]["message"]["chat"]
                ),
                raw=request["json"],
            )
