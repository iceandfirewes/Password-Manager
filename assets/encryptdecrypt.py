from Crypto.Cipher import AES 
import hashlib
def encrypt(hashedKey, plaintext):
    #create the cipher
    cipher = AES.new(hashedKey, AES.MODE_EAX)
    nonce = cipher.nonce
    data = str.encode(plaintext)
    #encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(data)
    #write the encrypted data in
    fd = open("passwordManagerData.dat","w+b")
    fd.write(ciphertext)
    fd.close()
    #write the nonce and tag
    fd = open("passwordManagerMetadata.dat", "w+b")
    fd.write(nonce)
    fd.write(tag)
    fd.close()
def decrypt(hashedKey, cipherText, nonce, tag):
    cipher = AES.new(hashedKey, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(cipherText)
    try:
        cipher.verify(tag)
        return plaintext
    except ValueError:
        return None
def getMetadata():
    fdMeta = open("passwordManagerMetadata.dat","rb")
    nonce = fdMeta.read(16)
    tag = fdMeta.read(16)
    fdMeta.close()
    return (nonce, tag)
