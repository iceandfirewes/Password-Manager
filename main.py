import PySimpleGUI as sg
import os.path
from assets.EncryptDecrypt import encrypt,returnMetadata
from assets.EntryForm import entryForm
import hashlib
#debug
encrypt(hashlib.sha256(str.encode("a")).digest(),f"name:company;username:me@gmail.com;password:password\nname:company;username:me@gmail.com;password:password")
# printMetaData()
#check if file exist
if os.path.isfile("passwordManagerData.dat"):
    entryForm(sg, False)
else:
    entryForm(sg, True)
