import PySimpleGUI as sg
import os.path
from assets.encryptdecrypt import encryptDecrypt, printMetaData
from assets.EntryForm import entryForm

#debug
encryptDecrypt()
# printMetaData()
#check if file exist
if os.path.isfile("passwordManagerData.dat"):
    entryForm(sg, False)
else:
    entryForm(sg, True)
