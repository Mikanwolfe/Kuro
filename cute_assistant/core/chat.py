from typing import Any, List, Dict
import openai

from cute_assistant.core.log import cute_logger as logger
from cute_assistant.core.database_utils import query_database


# Convert this into gated and pre-prompts
def apply_prompt_template(question: str) -> str:
    prompt = f"""
        By considering above input from me, answer the question: {question}
    """
    return prompt



def call_chatgpt_api(user_question: str, chunks: List[str]) -> Dict[str, Any]:
    # Send a request to the GPT-3 API
    messages = list(
        map(lambda chunk: {
            "role": "user",
            "content": chunk
        }, chunks))
    question = apply_prompt_template(user_question)
    messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=512,
        temperature=0.7,  # High temperature leads to a more creative response.
    )
    return response




def ask(user_question: str) -> Dict[str, Any]:
    # Get chunks from database.
    chunks_response = query_database(user_question)
    chunks = []
    for result in chunks_response["results"]:
        for inner_result in result["results"]:
            chunks.append(inner_result["text"])
    
    logger("chat").info("User's questions: %s", user_question)
    logger("chat").info("Retrieved chunks: %s", chunks)
    
    response = call_chatgpt_api(user_question, chunks)
    logger("chat").info("Response: %s", response)
    
    return response["choices"][0]["message"]["content"]