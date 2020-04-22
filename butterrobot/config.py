import os

# --- Butter Robot -----------------------------------------------------------------
DEBUG = os.environ.get("DEBUG", "n") == "y"

HOSTNAME = os.environ.get("BUTTERROBOT_HOSTNAME", "butterrobot-dev.int.fmartingr.network")

LOG_LEVEL = os.environ.get("LOG_LEVEL", "ERROR")

ENABLED_PLUGINS = os.environ.get("ENABLED_PLUGINS", "contrib/dev/ping").split(",")


# --- PLATFORMS ---------------------------------------------------------------------
# ---
# Slack
# ---
# Slack app access token
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

# Slack app oauth access token to send messages on the bot behalf
SLACK_BOT_OAUTH_ACCESS_TOKEN = os.environ.get("SLACK_BOT_OAUTH_ACCESS_TOKEN")

# ---
# Telegram
# ---
# Telegram auth token
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
