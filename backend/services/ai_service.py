import sys
from pathlib import Path
import anthropic
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.state import ai_messages
from backend.config import CLAUDE_API_KEY 
anthropic_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def generate_claude_message(message):

    ai_messages.append({
        'role': 'user',
        'content':message
    })
    response = anthropic_client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        messages=ai_messages
        )
    
    text_blocks = [block.text for block in response.content if block.type == "text"]
    clean_text = "\n".join(text_blocks)
    ai_messages.append({
        'role': 'assistant',
        'content':clean_text
    })
    return clean_text

