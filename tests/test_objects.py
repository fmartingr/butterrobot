from butterrobot.objects import Channel, ChannelPlugin


def test_channel_has_enabled_plugin_ok():
    channel = Channel(
        platform="debug",
        platform_channel_id="debug",
        channel_raw={},
        plugins={
            "enabled": ChannelPlugin(id=1, channel_id="test", plugin_id="enabled", enabled=True),
            "existant": ChannelPlugin(id=2, channel_id="test", plugin_id="existant"),
        }
    )
    assert not channel.has_enabled_plugin("non.existant")
    assert not channel.has_enabled_plugin("existant")
    assert channel.has_enabled_plugin("enabled")
