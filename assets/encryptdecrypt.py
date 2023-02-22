from Crypto.Cipher import AES 
import hashlib
def encryptDecrypt():
    hashedKey = hashlib.sha256(str.encode("a")).digest()
    cipher = AES.new(hashedKey, AES.MODE_EAX)
    nonce = cipher.nonce
    fd = open("passwordManagerData.dat","w+b")
    fd.write(b"dataABC")
    fd.close()
    data = b"dataABC"
    ciphertext, tag = cipher.encrypt_and_digest(data)
    fd = open("passwordManagerMetadata.dat", "w+b")
    fd.write(nonce)
    fd.write(tag)
    fd.close()
    print(f"ciphertext: {ciphertext}")
    print(f"nonce: {nonce} with {len(nonce)} length")
    print(f"tag: {tag} with {len(tag)} length")
    cipher = AES.new(hashedKey, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    print(plaintext)
    try:
        cipher.verify(tag)
        print("The message is authentic:", plaintext)
    except ValueError:
        print("Key incorrect or message corrupted")
def printMetaData():
    fdMeta = open("passwordManagerMetadata.dat","rb")
    nonce = fdMeta.read(16)
    tag = fdMeta.read(16)
    print(f"nonce: {nonce} with {len(nonce)} length")
    print(f"tag: {tag} with {len(tag)} length")
    fdMeta.close()