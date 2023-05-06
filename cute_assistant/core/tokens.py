import tiktoken
from tinydb import TinyDB, Query

# Calculations based on the ChatGPT Wrapper https://github.com/mmabrouk/chatgpt-wrapper

#TODO: Move this to the Nosql module
db_location = 'datastore/data.json'
db = TinyDB(db_location, indent=4, separators=(',', ': '))

messages_table = db.table('messages')

def format_memory(role, message):
    user = "Memory"
    msg = {
        "role" : role,
        "content" : f"{user} : {str(message)}"
    }
    return msg

# From the wrapper
def get_num_tokens(messages):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

def get_conversation_token_count(self, conversation_id=None):
    conversation_id = conversation_id or self.conversation_id
    success, old_messages, user_message = self.message.get_messages(conversation_id)
    if not success:
        raise Exception(user_message)
    token_messages = self.prepare_prompt_messsage_context(old_messages)
    tokens = self.get_num_tokens(token_messages)
    return tokens

def get_messages_until_token_limit(conversation_id, max_tokens):
    Message = Query()
    messages_in_convo = messages_table.search(Message.conversation_id == conversation_id)
    most_recent_messages = sorted(messages_in_convo, key=lambda convo: convo['created_time'])

    tokens = 0
    selected_messages = []
    print(f"Getting messages until token: {tokens}/{max_tokens}")
    for msg in reversed(most_recent_messages):

        msg_tokens = get_num_tokens([{"role": str(msg["role"]), "content": msg["message"]}])
        print(f"Getting messages until token: {tokens}/{max_tokens}")

        if tokens + msg_tokens <= max_tokens:
            tokens += msg_tokens
            selected_messages.insert(0, msg)
        else:
            break

    return selected_messages

def get_memory_until_token_limit(chunk_memories, max_tokens, max_mem_tokens=3192):
    relevant_memories = sorted(chunk_memories['results'][0]['results'], key=lambda memory: memory['score'])

    tokens = 0
    distant_tokens = 0
    selected_memories = []
    distant_memories = []
    for mem in reversed(relevant_memories):

        memory_message = [format_memory("user", mem['text'])]
        msg_tokens = get_num_tokens(memory_message)

        if tokens + msg_tokens <= max_tokens:
            tokens += msg_tokens
            selected_memories.insert(0, mem)
        elif distant_tokens + msg_tokens <= max_mem_tokens:
            distant_tokens += msg_tokens
            distant_memories.insert(0, mem)
        else:
            break

    return selected_memories, distant_memories
