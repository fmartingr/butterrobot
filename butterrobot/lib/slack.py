from typing import Optional, Text

import requests
import structlog

from butterrobot.config import SLACK_BOT_OAUTH_ACCESS_TOKEN


logger = structlog.get_logger()


class SlackAPI:
    BASE_URL = "https://slack.com/api"
    HEADERS = {"Authorization": f"Bearer {SLACK_BOT_OAUTH_ACCESS_TOKEN}"}

    class SlackError(Exception):
        pass

    class SlackClientError(Exception):
        pass

    @classmethod
    def get_conversations_info(cls, chat_id) -> dict:
        params = {"channel": chat_id}
        response = requests.get(
            f"{cls.BASE_URL}/conversations.info", params=params, headers=cls.HEADERS,
        )
        response_json = response.json()
        if not response_json["ok"]:
            raise cls.SlackClientError(response_json)

        return response_json["channel"]

    @classmethod
    def get_user_info(cls, chat_id) -> dict:
        params = {"user": chat_id}
        response = requests.get(
            f"{cls.BASE_URL}/users.info", params=params, headers=cls.HEADERS,
        )
        response_json = response.json()
        if not response_json["ok"]:
            raise cls.SlackClientError(response_json)

        return response_json["user"]

    @classmethod
    def send_message(cls, channel, message, thread: Optional[Text] = None):
        payload = {
            "text": message,
            "channel": channel,
        }

        if thread:
            payload["thread_ts"] = thread

        response = requests.post(
            f"{cls.BASE_URL}/chat.postMessage", data=payload, headers=cls.HEADERS,
        )
        response_json = response.json()
        if not response_json["ok"]:
            raise cls.SlackClientError(response_json)
