import sys
from pathlib import Path
import anthropic
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import CLAUDE_API_KEY 
anthropic_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def generate_claude_message(messages):

    response = anthropic_client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        messages=messages
        )
    text_blocks = [block.text for block in response.content if block.type == "text"]
    clean_text = "\n".join(text_blocks)

    return clean_text

