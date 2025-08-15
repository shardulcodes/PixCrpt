# app/reverse_tools.py
import os
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import tarfile

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def decrypt_data(encrypted: bytes, password: str) -> bytes:
    salt = encrypted[:16]
    iv = encrypted[16:32]
    ciphertext = encrypted[32:]
    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

def image_to_data(image_path: str) -> bytes:
    image = Image.open(image_path)
    data = np.array(image).reshape(-1, 3).flatten()
    return data.tobytes()

def recover_folder_from_image(image_path: str, output_folder: str, password: str) -> str:
    data = image_to_data(image_path)
    length = int.from_bytes(data[:4], byteorder='big')
    encrypted = data[4:4+length]

    decrypted = decrypt_data(encrypted, password)

    tar_path = "recovered.tar"
    with open(tar_path, "wb") as f:
        f.write(decrypted)

    os.makedirs(output_folder, exist_ok=True)
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(path=output_folder)
    os.remove(tar_path)

    return output_folder
