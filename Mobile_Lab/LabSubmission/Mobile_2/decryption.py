from Crypto.Cipher import AES
import base64

key_hex = "8d127684cbc37c17616d806cf50473cc"
key = bytes.fromhex(key_hex)

ciphertext_b64 = "5UJiFctbmgbDoLXmpL12mkno8HT4Lv8dlat8FxR2GOc="
ciphertext = base64.b64decode(ciphertext_b64)

cipher = AES.new(key, AES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print("Decrypted string:", plaintext.decode())
