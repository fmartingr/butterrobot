import requests
import structlog

from butterrobot.config import TELEGRAM_TOKEN


logger = structlog.get_logger(__name__)


class TelegramAPI:
    BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

    DEFAULT_ALLOWED_UPDATES = ["message"]

    class TelegramError(Exception):
        pass

    class TelegramClientError(Exception):
        pass

    @classmethod
    def set_webhook(cls, webhook_url, max_connections=40, allowed_updates=None):
        allowed_updates = allowed_updates or cls.DEFAULT_ALLOWED_UPDATES
        url = f"{cls.BASE_URL}/setWebhook"
        payload = {
            "url": webhook_url,
            "max_connections": max_connections,
            "allowed_updates": allowed_updates,
        }
        response = requests.post(url, json=payload)
        response_json = response.json()
        if not response_json["ok"]:
            raise cls.TelegramClientError(response_json)

    @classmethod
    def send_message(
        cls,
        chat_id,
        text,
        parse_mode="markdown",
        disable_web_page_preview=False,
        disable_notification=False,
        reply_to_message_id=None,
    ):
        url = f"{cls.BASE_URL}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
        }

        response = requests.post(url, json=payload)
        response_json = response.json()
        if not response_json["ok"]:
            raise cls.TelegramClientError(response_json)
