from cryptography.fernet import Fernet

key = Fernet.generate_key()

def encrypt_id(id):
    cipher = Fernet(key)
    encrypted = id.encode('utf-8')
    return cipher.encrypt(encrypted).decode('utf-8')


def decrypt_id(encrypted_id):
    cipher = Fernet(key)
    id = cipher.decrypt(encrypted_id.encode('utf-8'))
    return id.decode('utf-8')
