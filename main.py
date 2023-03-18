import PySimpleGUI as sg
import os.path
from assets.EncryptDecrypt import encrypt,returnMetadata
from assets.EntryForm import entryForm
import hashlib
#debug
encrypt(hashlib.sha256(str.encode("a")).digest(),f"name:companyA;username:meA@gmail.com;password:passwordA;comment:A\nname:companyB;username:meB@gmail.com;password:passwordB;comment:B")
# printMetaData()
#check if file exist
if os.path.isfile("passwordManagerData.dat"):
    entryForm(sg, False)
else:
    entryForm(sg, True)
