
import json
from cute_assistant.core import client

settings_file = 'datastore/settings.json'

def main():
    with open(settings_file) as f:
        settings = json.load(f)

    client.run_bot(settings['kuro_api_key'])

if __name__ == "__main__":
    main()