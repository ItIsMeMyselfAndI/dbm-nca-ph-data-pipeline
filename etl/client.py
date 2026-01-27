import os
import sys
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")


if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    sys.exit()

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
