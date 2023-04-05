import PySimpleGUI as sg
import os.path
from assets.EntryForm import entryForm
from assets.versionControl import versionCheck
#DEBUG
# import hashlib
# from assets.EncryptDecrypt import encrypt,getMetadata
# data = f"""name\x1fcompanyA\x1eusername\x1fmeA@gmail.com\x1epassword\x1fpasswordA\x1ecomment\x1fA\x1d
# name\x1fcompanyB\x1eusername\x1fmeB@gmail.com\x1epassword\x1fpasswordB\x1ecomment\x1fB"""
# # print(data.split("\x1d"))
# encrypt(hashlib.sha256(str.encode("a")).digest(),data)
# getMetadata()
#check version file
# if versionCheck(sg):
    #check if files exist
if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
    entryForm(sg, False)
else:
    entryForm(sg, True)