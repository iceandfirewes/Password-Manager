# from Crypto.Cipher import AES 
# cipher = AES.new(hashedKey, AES.MODE_EAX)
# nonce = cipher.nonce
# fd = open("passwordManagerNonce.dat", "w+b")
# fd.write(nonce)
# fd.close()
# data = str.encode("abcASDWEEEEEEEEEEEEEEEEEEEEE")
# ciphertext, tag = cipher.encrypt_and_digest(data)
# print(ciphertext)
# cipher = AES.new(hashedKey, AES.MODE_EAX, nonce=nonce)
# plaintext = cipher.decrypt(ciphertext)
# try:
#     cipher.verify(tag)
#     print("The message is authentic:", plaintext)
# except ValueError:
#     print("Key incorrect or message corrupted")
# #fd.write(sha256.decode("utf-8"))