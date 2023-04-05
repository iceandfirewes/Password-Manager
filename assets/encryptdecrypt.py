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
    fd = open("passwordManagerData.dat","wb")
    fd.write(ciphertext)
    fd.close()
    #write the nonce and tag
    fd = open("passwordManagerMetadata.dat", "wb")
    fd.write(nonce)
    fd.write(tag)
    fd.close()
def decrypt(hashedKey):
    fd = open("passwordManagerData.dat","rb")
    cipherText = fd.read()
    fd.close()
    nonce,tag  = getMetadata()
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
def encryptTest(hashedKey, plaintext):
#create the cipher
    cipher = AES.new(hashedKey, AES.MODE_EAX)
    nonce = cipher.nonce
    data = str.encode(plaintext)
    #encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(data)
    #write the encrypted data in
    fd = open("passwordManagerTestData.dat","wb")
    fd.write(ciphertext)
    fd.close()
    #write the nonce and tag
    fd = open("passwordManagerTestMetadata.dat", "wb")
    fd.write(nonce)
    fd.write(tag)
    fd.close()
def decryptTest(hashedKey):
    fd = open("passwordManagerTestData.dat","rb")
    cipherText = fd.read()
    fd.close()
    nonce,tag  = getMetadataTest()
    cipher = AES.new(hashedKey, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(cipherText)
    try:
        cipher.verify(tag)
        return plaintext
    except ValueError:
        return None
def getMetadataTest():
    fdMeta = open("passwordManagerTestMetadata.dat","rb")
    nonce = fdMeta.read(16)
    tag = fdMeta.read(16)
    fdMeta.close()
    return (nonce, tag)