def assemble_openai_request(user_messages, system_prompt, additional_prompts, i):
    # Insert the system prompt and additional prompts after the ith most recent message
    assembled_messages = user_messages.copy()
    assembled_messages.insert(-i, system_prompt)
    assembled_messages.insert(-i, additional_prompts)

    # Assemble the messages into a single string to send to the OpenAI API
    assembled_request = " ".join(assembled_messages)

    return assembled_request

# Example usage
user_messages = [
    "User: Hi",
    "User: How are you?",
    "User: Can you help me?",
    "User: Thanks!",
]

system_prompt = "System: I'm here to help!"
additional_prompts = "System: What do you need assistance with?"

# Insert the system and additional prompts after the 2nd most recent message
assembled_request = assemble_openai_request(user_messages, system_prompt, additional_prompts, 2)

print(assembled_request)
