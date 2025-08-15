# app/stego_tools.py
import os
import tarfile
import numpy as np
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets

def compress_folder(folder_path: str, output_tar: str):
    with tarfile.open(output_tar, "w") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_data(data: bytes, password: str):
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    iv = secrets.token_bytes(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    encrypted_data = salt + iv + ciphertext
    length = len(encrypted_data).to_bytes(4, byteorder='big')
    return length + encrypted_data

def data_to_image(data: bytes, output_path: str):
    byte_array = np.frombuffer(data, dtype=np.uint8)
    padding = (-len(byte_array)) % 3
    if padding:
        byte_array = np.concatenate([byte_array, np.zeros(padding, dtype=np.uint8)])

    pixels = byte_array.reshape((-1, 3))
    side = int(np.ceil(np.sqrt(len(pixels))))
    padded = side * side - len(pixels)

    if padded > 0:
        pixels = np.vstack([pixels, np.zeros((padded, 3), dtype=np.uint8)])

    image_array = pixels.reshape((side, side, 3))
    image = Image.fromarray(image_array.astype(np.uint8), mode='RGB')
    image.save(output_path)

def folder_to_secure_image(folder_path: str, output_image_path: str, password: str):
    compress_folder(folder_path, "temp.tar")
    with open("temp.tar", "rb") as f:
        tar_data = f.read()
    os.remove("temp.tar")

    encrypted = encrypt_data(tar_data, password)
    data_to_image(encrypted, output_image_path)
