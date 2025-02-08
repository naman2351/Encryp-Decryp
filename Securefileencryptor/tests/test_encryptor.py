import os
import unittest
from encryption_tool.encrypt import encrypt_file
from encryption_tool.decrypt import decrypt_file

class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        self.encrypted_file = self.test_file + ".enc"
        self.decrypted_file = "test_file_decrypted.txt"
        self.password = "testpassword123"
        
        # Create a sample file for testing
        with open(self.test_file, "w") as f:
            f.write("This is a test.")

    def test_encryption_decryption(self):
        # Encrypt the file
        encrypt_file(self.test_file, self.password)
        self.assertTrue(os.path.exists(self.encrypted_file))

        # Decrypt the file
        decrypt_file(self.encrypted_file, self.password)
        self.assertTrue(os.path.exists(self.decrypted_file))

        # Verify contents match
        with open(self.test_file, "r") as f1, open(self.decrypted_file, "r") as f2:
            self.assertEqual(f1.read(), f2.read())

    def tearDown(self):
        # Cleanup test files
        os.remove(self.test_file)
        if os.path.exists(self.encrypted_file):
            os.remove(self.encrypted_file)
        if os.path.exists(self.decrypted_file):
            os.remove(self.decrypted_file)

if __name__ == "__main__":
    unittest.main()
