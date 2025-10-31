"""
Simple Supabase Connection Test
Quick test to verify everything is working
"""

from supabase_db import get_db
from datetime import datetime, date

print("\n" + "="*60)
print("✅ SUPABASE CONNECTION TEST")
print("="*60 + "\n")

# Initialize database
db = get_db()

# Test connection
print("1. Testing PostgreSQL connection...")
if db.test_connection():
    print("   ✅ SUCCESS!\n")
else:
    print("   ❌ FAILED!\n")
    exit(1)

# Create tables
print("2. Creating database tables...")
db.init_database()
print("   ✅ Tables created!\n")

print("="*60)
print("✅ SUPABASE IS READY TO USE!")
print("="*60)
print("\n📌 You can now:")
print("   - Add students using Supabase API or PostgreSQL")
print("   - Mark attendance")
print("   - View reports")
print("   - All data syncs with Supabase cloud")
print("\n" + "="*60 + "\n")
