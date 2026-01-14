import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


def get_supabase_client() -> Client:
    """Supabase 클라이언트 인스턴스 반환"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")

    return create_client(url, key)


# 싱글톤 인스턴스
_supabase_client: Client | None = None


def get_client() -> Client:
    """싱글톤 Supabase 클라이언트 반환"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = get_supabase_client()
    return _supabase_client
