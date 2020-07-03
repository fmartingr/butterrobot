from typing import Optional, Text

import aiohttp
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
    async def send_message(cls, channel, message, thread: Optional[Text] = None):
        payload = {
            "text": message,
            "channel": channel,
        }

        if thread:
            payload["thread_ts"] = thread

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{cls.BASE_URL}/chat.postMessage",
                data=payload,
                headers={"Authorization": f"Bearer {SLACK_BOT_OAUTH_ACCESS_TOKEN}"},
            ) as response:
                response = await response.json()
                if not response["ok"]:
                    raise cls.SlackClientError(response)
