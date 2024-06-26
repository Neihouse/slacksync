import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from .commands import register_commands
from .utils import setup_database  # Assuming you have a setup_database function

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# App initialization
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Database setup (create tables if they don't exist)
setup_database()  

# Register commands from commands.py
register_commands(app)

# Error Handling
@app.error
def handle_error(error, logger):
    logger.error(f"Error: {error}")

# Socket Mode Handler
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
