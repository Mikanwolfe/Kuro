import logging
from discord import Webhook
import aiohttp

class DiscordLoggingHandler(logging.Handler):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

    def emit(self, record):
        try:
            with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(self.webhook_url, session=session)
                webhook.send('Hello World')
            webhook = Webhook.from_url(self.webhook_url)

            log_entry = self.format(record)
            webhook.send(log_entry)

        except Exception as e:
            print(f"Error sending log to Discord: {e}")