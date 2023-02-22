from Crypto.Cipher import AES 
import hashlib
def encrypt():
    #create the hashed key and cipher
    hashedKey = hashlib.sha256(str.encode("a")).digest()
    cipher = AES.new(hashedKey, AES.MODE_EAX)
    nonce = cipher.nonce
    data = b"dataABC"
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
    print(f"hashedKey: {hashedKey}")
    print(f"ciphertext: {ciphertext}")
    print(f"nonce: {nonce} with {len(nonce)} length")
    print(f"tag: {tag} with {len(tag)} length")
    # decrypt(hashedKey, ciphertext, nonce, tag)

def decrypt(hashedKey, ciphertext, nonce, tag):
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