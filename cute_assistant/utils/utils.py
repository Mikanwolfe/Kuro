import re

def format_memory(role, message):
    user = "Memory"
    msg = {
        "role" : role,
        "content" : f"{user} : {str(message)}"
    }
    return msg

def format_discord_tag(user):
    formatted_tag = f"{user.display_name} ({str(user)})"
    return formatted_tag

def format_message(message, role, user, preprompt=None):
    if preprompt:
        content = f"{preprompt} : {format_discord_tag(user)} : {str(message)}"
    else:
        content = f"{format_discord_tag(user)} : {str(message)}"
    msg = {
        "role" : role,
        "content" : content
    }
    return msg

def remove_links(s: str) -> str:
    # Remove markdown image links
    s = re.sub(r"!\[.*?\]", "", s)
    
    # Remove wikilinks
    s = re.sub(r"\[\[.*?\]\]", "", s)
    
    # Remove markdown links
    s = re.sub(r"\[.*?\]\(.*?\)", "", s)

    # Remove markdown heading tags
    s = re.sub(r"#+", "", s)

    # Remove markdown line break formatting
    s = re.sub(r"\*{3,4}|-{3,4}", "", s)

    # Remove URLs
    s = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', s)
    
    return s

def remove_phrases_from_string(phrases, text):
    for phrase in phrases:
        text = text.replace(phrase, '')
    return text

async def check_privilege(user_id: int, level: str, settings: dict) -> bool:
    level_users = settings.get(level, [])
    return user_id in level_users