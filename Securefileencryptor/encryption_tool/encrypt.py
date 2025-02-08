from Crypto.Cipher import AES
import os
import hashlib

def encrypt_file(file_path, password):
    """
    Encrypts a file using AES-256 encryption.
    :param file_path: Path to the file to be encrypted
    :param password: User-provided password for encryption
    """
    try:
        # Read the file data
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Derive a 32-byte encryption key from the password
        key = hashlib.sha256(password.encode()).digest()
        
        # Create cipher object
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        
        # Encrypt data
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # Save the encrypted file
        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, 'wb') as f:
            f.write(nonce + tag + ciphertext)
        
        print(f"File encrypted successfully: {encrypted_file_path}")
    
    except Exception as e:
        print(f"Encryption failed: {e}")

# Example usage
if __name__ == "__main__":
    file_to_encrypt = input("Enter the file path to encrypt: ")
    user_password = input("Enter a password: ")
    encrypt_file(file_to_encrypt, user_password)