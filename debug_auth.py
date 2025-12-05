import sys
sys.path.insert(0, '.')

print("Debugging authentication...")

# Check imports
try:
    from app.auth import authenticate_user, get_password_hash, get_user
    print("✅ Auth functions imported")
    
    # Check if default users exist
    from app.db import db
    print(f"✅ Database has {len(db.users)} users")
    
    # Try to authenticate
    user = authenticate_user("john_doe", "password123")
    if user:
        print(f"✅ Authentication successful for john_doe: {user.username}")
    else:
        print("❌ Authentication failed for john_doe")
        
    # Check password hashing
    test_hash = get_password_hash("test123")
    print(f"✅ Password hashing works")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
