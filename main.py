import PySimpleGUI as sg
import os.path
from assets.EntryForm import entryForm
#check if file exist
if os.path.isfile("password-manager-data.dat"):
    entryForm(sg, False)
else:
    entryForm(sg, True)
