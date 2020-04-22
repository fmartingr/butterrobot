from datetime import datetime

import structlog

from butterrobot.platforms.base import Platform, PlatformMethods
from butterrobot.config import TELEGRAM_TOKEN, HOSTNAME
from butterrobot.lib.telegram import TelegramAPI
from butterrobot.objects import Message


logger = structlog.get_logger(__name__)


class TelegramMethods(PlatformMethods):
    @classmethod
    async def send_message(self, message: Message):
        logger.debug(
            "Outgoing message", message=message.__dict__, platform=TelegramPlatform.ID
        )
        await TelegramAPI.send_message(
            chat_id=message.chat,
            text=message.text,
            reply_to_message_id=message.reply_to,
        )


class TelegramPlatform(Platform):
    ID = "telegram"

    methods = TelegramMethods

    @classmethod
    async def init(cls, app):
        """
        Initializes the Telegram webhook endpoint to receive updates
        """

        if not TELEGRAM_TOKEN:
            logger.error("Missing token. platform not enabled.", platform=cls.ID)
            return

        webhook_url = f"https://{HOSTNAME}/telegram/incoming/{TELEGRAM_TOKEN}"
        try:
            await TelegramAPI.set_webhook(webhook_url)
        except TelegramAPI.TelegramError as error:
            logger.error(f"Error setting Telegram webhook: {error}", platform=cls.ID)
            raise Platform.PlatformInitError()

    @classmethod
    async def parse_incoming_message(cls, request):
        token = request.path.split("/")[-1]
        if token != TELEGRAM_TOKEN:
            raise cls.PlatformAuthError("Authentication error")

        request_data = await request.get_json()
        logger.debug("Parsing message", data=request_data, platform=cls.ID)

        if "text" in request_data["message"]:
            # Ignore all messages but text messages
            return Message(
                id=request_data["message"]["message_id"],
                date=datetime.fromtimestamp(request_data["message"]["date"]),
                text=str(request_data["message"]["text"]),
                chat=str(request_data["message"]["chat"]["id"]),
                raw=request_data,
            )
