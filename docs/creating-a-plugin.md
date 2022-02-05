# Creating a Plugin

## Example

This simple "Marco Polo" plugin will answer _Polo_ to the user that say _Marco_:

``` python
# mypackage/plugins.py
from butterrobot.plugins import Plugin
from butterrobot.objects import Message


class PingPlugin(Plugin):
    name = "Marco/Polo"
    id = "test.marco"

    @classmethod
    def on_message(cls, message, **kwargs):
        if message.text == "Marco":
            yield Message(
                chat=message.chat, reply_to=message.id, text=f"polo",
            )
```

``` python
# setup.py
# ...
entrypoints = {
    "test.marco" = "mypackage.plugins:MarcoPlugin"
}

setup(
    # ...
    entry_points=entrypoints,
    # ...
)
```
