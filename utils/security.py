# utils/security.py
import os
from cryptography.fernet import Fernet

KEY_FILE = 'data/secret.key'

# Generate a key and save it (do this once)
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    return open(KEY_FILE, 'rb').read()

def encrypt_pdf(pdf_path):
    key = load_key()
    fernet = Fernet(key)
    with open(pdf_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(pdf_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_pdf(pdf_path):
    key = load_key()
    fernet = Fernet(key)
    with open(pdf_path, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    return decrypted

# generate_key()