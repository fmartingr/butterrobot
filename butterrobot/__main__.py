from butterrobot.app import app
from butterrobot.config import DEBUG

# Only used for local development!
# python -m butterrobot
app.run(debug=DEBUG, host="0.0.0.0")
