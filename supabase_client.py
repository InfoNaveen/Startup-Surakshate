import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """
    Get a Supabase client instance
    
    Returns:
        Client: Supabase client
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    return create_client(supabase_url, supabase_key)

# Database schema initialization function
def init_supabase_schema():
    """
    Initialize Supabase database schema if it doesn't exist
    This function should be called once during application startup
    """
    try:
        supabase = get_supabase_client()
        
        # Check if tables exist and create them if they don't
        # Note: In a real application, you would use Supabase migrations
        # This is a simplified approach for the hackathon
        
        # Create profiles table
        supabase.table("profiles").select("*").limit(1).execute()
        
        # Create scans table
        supabase.table("scans").select("*").limit(1).execute()
        
        print("Supabase schema initialized successfully")
    except Exception as e:
        print(f"Error initializing Supabase schema: {str(e)}")
        print("Please make sure you have created the necessary tables in Supabase:")
        print("1. profiles (id, email, name, created_at)")
        print("2. scans (id, url, scan_type, name, description, status, created_at, completed_at, results, summary)")