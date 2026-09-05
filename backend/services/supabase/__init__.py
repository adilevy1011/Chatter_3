from supabase import create_client, Client
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.config import SUPABASE_ANON_KEY, SUPABASE_URL

url: str = SUPABASE_URL
key: str = SUPABASE_ANON_KEY
supabase: Client = create_client(url, key)