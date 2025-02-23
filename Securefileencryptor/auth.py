import bcrypt
from sqlalchemy.orm import Session
from database import SessionLocal, User

def add_user(username: str, password: str):
    """Register a new user with hashed password."""
    session = SessionLocal()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        user = User(username=username, password_hash=hashed_password)
        session.add(user)
        session.commit()
        print(f"✅ User '{username}' registered successfully.")
    except Exception as e:
        session.rollback()
        print(f"⚠️ Error registering user: {e}")
    finally:
        session.close()

def authenticate_user(username: str, password: str) -> bool:
    """Verify if username and password match in the database."""
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()

    if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return True
    return False
