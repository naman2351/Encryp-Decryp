from Crypto.Cipher import AES
import os
import hashlib

def decrypt_file(file_path, password):
    """
    Decrypts a file using AES-256 encryption.
    :param file_path: Path to the encrypted file
    :param password: User-provided password for decryption
    """
    try:
        # Read the encrypted file
        with open(file_path, 'rb') as f:
            nonce = f.read(16)  # First 16 bytes for nonce
            tag = f.read(16)    # Next 16 bytes for authentication tag
            ciphertext = f.read()  # Remaining bytes are encrypted data

        # Derive a 32-byte encryption key from the password
        key = hashlib.sha256(password.encode()).digest()
        
        # Create a cipher object
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        
        # Attempt decryption
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        
        # Save the decrypted file
        decrypted_file_path = file_path.replace(".enc", "_decrypted")
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted_data)

        print(f"File decrypted successfully: {decrypted_file_path}")
    except ValueError:
        print("Error: Incorrect password or corrupted file!")
    except Exception as e:
        print(f"Decryption failed: {e}")

# Example usage
if __name__ == "__main__":
    file_to_decrypt = input("Enter the encrypted file path: ")
    user_password = input("Enter the password: ")
    decrypt_file(file_to_decrypt, user_password)
