import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def decrypt_file(file_path, password):
    with open(file_path, "rb") as f:
        data = f.read()

    # Extract salt, IV, and ciphertext
    salt, iv, ciphertext = data[:16], data[16:32], data[32:]

    # Derive the key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Set up AES decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]

    # Restore original file extension
    original_file_path = file_path.replace(".encrypted", "")

    with open(original_file_path, "wb") as f:
        f.write(decrypted_data)

    print(f"File decrypted successfully: {original_file_path}")

# Example usage
if __name__ == "__main__":
    file_to_decrypt = input("Enter the encrypted file path: ")
    user_password = input("Enter the password: ")
    decrypt_file(file_to_decrypt, user_password)
