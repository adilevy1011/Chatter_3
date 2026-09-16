import sys
from pathlib import Path
import anthropic
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import CLAUDE_API_KEY 
anthropic_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def generate_claude_message(messages,thinking_on = False):
    if thinking_on:
        response = anthropic_client.messages.create(
            model="claude-opus-5",
            thinking={"type": "adaptive", "display": "summarized"},
            max_tokens=1024,
            messages=messages
        )
        thinking_blocks = [block.thinking for block in response.content if block.type == "thinking"]
        text_blocks = [block.text for block in response.content if block.type == "text"]
        clean_thinking_text = "\n".join(thinking_blocks)
        clean_text = "\n".join(text_blocks)

        return {"thinking":clean_thinking_text,"response":clean_text}
    else:
        response = anthropic_client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            messages=messages
        )
        text_blocks = [block.text for block in response.content if block.type == "text"]
        clean_text = "\n".join(text_blocks)

        return {"response":clean_text}

def generate_chat_title(messages):
    response = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="""
        You are a title generator. Write a short title (2-5 words) summarizing the beginning of this conversation.
        DO NOT include any markdown. The title should be a summary of the tone of the conversation, attempting to predict what the user would be talking about. If there a clear topic, use it. If there is no clear topic use something simple and general.
        """,
        messages=messages
    )
    text_blocks = [block.text for block in response.content if block.type == "text"]
    clean_text = "\n".join(text_blocks)
    return clean_text