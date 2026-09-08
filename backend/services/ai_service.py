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
            model="claude-opus-5",
            max_tokens=1024,
            messages=messages
        )
        text_blocks = [block.text for block in response.content if block.type == "text"]
        clean_text = "\n".join(text_blocks)

        return {"response":clean_text}
