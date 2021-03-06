from datetime import datetime
from dataclasses import dataclass, field
from typing import Text, Optional


@dataclass
class Message:
    text: Text
    chat: Text
    author: Text = None
    from_bot: bool = False
    date: Optional[datetime] = None
    id: Optional[Text] = None
    reply_to: Optional[Text] = None
    raw: dict = field(default_factory=dict)
