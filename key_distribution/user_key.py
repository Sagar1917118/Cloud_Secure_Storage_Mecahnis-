from hashlib import pbkdf2_hmac
import hmac
import hashlib

def derive_user_key(password: str, salt: bytes = b'some_salt', iterations: int = 100000) -> bytes:
    """Derive a secure user key from password using PBKDF2 (SHA-256)"""
    return pbkdf2_hmac('sha256', password.encode(), salt, iterations, dklen=32)

password = input("Enter your password: ")
user_key = derive_user_key(password)
print("\n User Key (hex):", user_key.hex())
