from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

key_hex = "8d127684cbc37c17616d806cf50473cc"
key = bytes.fromhex(key_hex)

ciphertext_b64 = "5UJiFctbmgbDoLXmpL12mkno8HT4Lv8dlat8FxR2GOc="
ciphertext = base64.b64decode(ciphertext_b64)

cipher = Cipher(
    algorithms.AES(key),
    modes.ECB()
)

decryptor = cipher.decryptor()
padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

unpadder = padding.PKCS7(128).unpadder()
plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

print("Decrypted bytes:", plaintext)
print("Decrypted string:", plaintext.decode())