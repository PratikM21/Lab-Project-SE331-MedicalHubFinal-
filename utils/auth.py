import pandas as pd
import os
from passlib.context import CryptContext

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database file path
USERS_DB = "users.csv"

def get_password_hash(password: str) -> str:
    """Generate a secure password hash using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_users_df() -> pd.DataFrame:
    """Load or create users dataframe"""
    if os.path.exists(USERS_DB):
        return pd.read_csv(USERS_DB)
    return pd.DataFrame(columns=["username", "email", "full_name", "hashed_password"])

def save_users_df(df: pd.DataFrame) -> None:
    """Save users dataframe to CSV"""
    df.to_csv(USERS_DB, index=False)

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user with username and password"""
    df = get_users_df()
    user = df[df["username"] == username]
    
    if not user.empty:
        hashed_password = user.iloc[0]["hashed_password"]
        return verify_password(password, hashed_password)
    return False

def register_user(username: str, password: str, email: str, full_name: str = None) -> bool:
    """Register a new user with hashed password"""
    df = get_users_df()
    
    # Check if username already exists
    if username in df["username"].values:
        return False
    
    # Create new user record
    new_user = pd.DataFrame([{
        "username": username,
        "email": email,
        "full_name": full_name,
        "hashed_password": get_password_hash(password)
    }])
    
    # Save updated dataframe
    updated_df = pd.concat([df, new_user], ignore_index=True)
    save_users_df(updated_df)
    return True

def user_exists(username: str) -> bool:
    """Check if a username exists in the database"""
    df = get_users_df()
    return username in df["username"].values