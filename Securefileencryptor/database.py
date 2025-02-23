from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from datetime import datetime

# Database URL for SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base class for ORM models
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

# Define FileLogs model
class FileLogs(Base):
    __tablename__ = "file_logs"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    action = Column(String, nullable=False)  # "Encryption" or "Decryption"
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create database tables
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")

if __name__ == "__main__":
    create_tables()
