import PySimpleGUI as sg
import os.path
from assets.encryptdecrypt import encrypt, printMetaData
from assets.EntryForm import entryForm
#debug
encrypt("a","name:company;email:me@gmail.com;password:password")
# printMetaData()
#check if file exist
if os.path.isfile("passwordManagerData.dat"):
    entryForm(sg, False)
else:
    entryForm(sg, True)
