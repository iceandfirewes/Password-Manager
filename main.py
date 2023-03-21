import PySimpleGUI as sg
import os.path
from assets.EntryForm import entryForm
#DEBUG
# import hashlib
# from assets.EncryptDecrypt import encrypt,getMetadata
# encrypt(hashlib.sha256(str.encode("a")).digest(),f"name:companyA;username:meA@gmail.com;password:passwordA;comment:A\nname:companyB;username:meB@gmail.com;password:passwordB;comment:B")
# getMetadata()

#check if files exist
if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
    entryForm(sg, False)
else:
    entryForm(sg, True)
