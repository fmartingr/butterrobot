from typing import Optional, Text

import requests
import structlog

from butterrobot.config import SLACK_BOT_OAUTH_ACCESS_TOKEN


logger = structlog.get_logger()


class SlackAPI:
    BASE_URL = "https://slack.com/api"

    class SlackError(Exception):
        pass

    class SlackClientError(Exception):
        pass

    @classmethod
    def send_message(cls, channel, message, thread: Optional[Text] = None):
        payload = {
            "text": message,
            "channel": channel,
        }

        if thread:
            payload["thread_ts"] = thread

        response = requestts.post(
                f"{cls.BASE_URL}/chat.postMessage",
                data=payload,
                headers={"Authorization": f"Bearer {SLACK_BOT_OAUTH_ACCESS_TOKEN}"},
            )
        response_json = response.json()
        if not response_json["ok"]:
            raise cls.SlackClientError(response_json)
