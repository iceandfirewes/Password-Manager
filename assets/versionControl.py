import os
import json
import hashlib
from .EncryptDecrypt import encryptTest, decrypt
version = "1.3.0"
def versionCheck(sg):
    if not os.path.isfile("passwordManagerVersion.txt"):
        with open("passwordManagerVersion.txt","w") as fd:
            fd.write(version)
    #if exist
    else:
        #version control
        with open("passwordManagerVersion.txt","r") as fd:
            if(fd.readline() == "1.3.0"):
                handle130(sg)
def handle130(sg):
    if os.path.isfile("passwordManagerRawData.json"):
        #modify the json
        with open("passwordManagerRawData.json","r") as fd:
            data = json.load(fd)
            for index, password in enumerate(data["passwords"]):
                data["passwords"][index] = {"id":index, **password}
        #ask for masterkey
        masterKey = sg.popup_get_text('Old data file found, Please enter your masterkey', title="Data Update")
        hashedKey = hashlib.sha256(str.encode(masterKey)).digest()
        if decrypt(hashedKey):
            #verified. override time
            plaintext = json.dumps(data)
            #######################MAKE SURE TO REPLACE THIS WITH encrypt and make encrypt encryptTest
            encryptTest(hashedKey, plaintext)