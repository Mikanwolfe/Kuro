from tinydb import TinyDB, Query
from datetime import datetime

db_location = 'datastore/data.json'
db = None
conversations_table = None
messages_table = None
users_table = None

vdb_location = 'datastore/memories.json'
vdb = None

# Initialize the database
db = TinyDB(db_location, indent=4, separators=(',', ': '))
vdb = TinyDB(vdb_location, indent=4, separators=(',', ': '))

# Tables for Conversations, Messages, and Users
conversations_table = db.table('conversations')
messages_table = db.table('messages')
users_table = db.table('users')
channels_table = db.table("channel")
files_table = db.table('files')

# Table for vdb information
memory_table = vdb.table('memories')

User = Query()
Conversation = Query()
Message = Query()
Channel = Query()

Memory = Query()

def drop_tables():
    messages_table.truncate()
    conversations_table.truncate()

def create_channel(channel_id: int, allowed: bool = True):
    channels_table.insert({"channel_id": channel_id, "allowed": allowed})

def read_channel(channel_id: int):
    return channels_table.search(Channel.channel_id == channel_id)

def update_channel(channel_id: int, allowed: bool):
    channels_table.update({"allowed": allowed}, Channel.channel_id == channel_id)

def delete_channel(channel_id: int):
    channels_table.remove(Channel.channel_id == channel_id)

def add_memory(memory_id: str, content: str):
    memory_table.insert({"memory_id": memory_id, "content": content})

def delete_memory(memory_id: str):
    memory_table.remove(Memory.memory_id == memory_id)

def get_channel_type(channel_id: int):
    channel = channels_table.search(Channel.channel_id == channel_id)
    if not channel:
        return "None"
    return channel[0].get("type", "None")

def set_channel_type(channel_id: int, type: str):
    channels_table.update({"type": type}, Channel.channel_id == channel_id)

def get_channel_setting(channel_id: int, setting: str, default="None"):
    channel = channels_table.search(Channel.channel_id == channel_id)
    if not channel:
        return default
    return channel[0].get(setting, default)

def set_channel_setting(channel_id: int, setting: str, value: str):
    channels_table.update({setting: value}, Channel.channel_id == channel_id)

def save_file_content(file_name, content):
    file_entry = {
        'file_name': file_name,
        'content': content
    }
    files_table.insert(file_entry)

def get_all_channels():
    return channels_table.all()

def is_channel_allowed(channel_id: int):
    channel = channels_table.search(Channel.channel_id == channel_id)
    if not channel:
        return False
    return channel[0]["allowed"]

def set_db_location(location):
    global db_location, db, conversations_table, messages_table, users_table
    db_location = location
    db = TinyDB(db_location)
    conversations_table = db.table('conversations')
    messages_table = db.table('messages')
    users_table = db.table('users')

def add_conversation(title :str, channel_id: str) -> int:
    # Get the highest conversation ID (if exists) and increment it by 1
    highest_convo_id = max(conversations_table.all(), key=lambda x: x['conversation_id'], default={'conversation_id': 0})['conversation_id']
    new_convo_id = highest_convo_id + 1

    conversations_table.insert({
        'conversation_id': new_convo_id, 
        'title': title, 
        'created_time': datetime.now().isoformat(),
        'channel_id': channel_id
        })
    return new_convo_id

def get_most_recent_conversation(channel_id: int):
    # Define a query to filter conversations by channel_id
    Convo = Query()
    matching_conversations = conversations_table.search(Convo.channel_id == channel_id)
    if not matching_conversations:
        # no convos make a new one and return id
        id = add_conversation("Convo name for now", channel_id)
        matching_conversations = conversations_table.search(Convo.channel_id == channel_id)

    # Sort the conversations by created_time and return the most recent one
    most_recent_convo = sorted(matching_conversations, key=lambda convo: convo['created_time'], reverse=True)[0]
    return most_recent_convo



def add_user(name, uid, preference, nickname, discord_tag):
    user = {
        'name': name,
        'uid': uid,
        'preference': preference,
        'nickname': nickname,
        'discord_tag': discord_tag,
    }
    return users_table.insert(user)


def add_message(conversation_id, user_id, role, message):
    message = {
        'conversation_id': conversation_id,
        'user_id': user_id,
        'role': role,
        'message': message,
        'created_time': datetime.now().isoformat()
    }
    return messages_table.insert(message)


def get_messages_by_role(conversation_id, role):
    Message = Query()
    result = messages_table.search(
        (Message.conversation_id == conversation_id) & (Message.role == role)
    )
    return result

def get_last_messages_from_convo(conversation_id, numMessages):
    Message = Query()
    messages_in_convo = messages_table.search(Message.conversation_id == conversation_id)
    most_recent_messages = sorted(messages_in_convo, key=lambda convo: convo['created_time'])
    
    last_messages = most_recent_messages[-numMessages:] if len(most_recent_messages) > numMessages else most_recent_messages
    return last_messages

