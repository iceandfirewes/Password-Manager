import os
from .encryptdecrypt import decrypt
from Crypto.Cipher import AES 
def verify(sg, hashedKey):
    passwords = []
    #if files exists, verifying
    if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
        #read the metadata and the ciphertext
        print("password file exists. verifying...")
        fdMeta = open("passwordManagerMetadata.dat","rb")
        nonce = fdMeta.read(16)
        tag = fdMeta.read(16)
        fdMeta.close()
        fd = open("passwordManagerData.dat","rb")
        cipherText = fd.read()
        fd.close()
        if(plaintext := decrypt(hashedKey, cipherText, nonce, tag)):
            print("The message is authentic:", plaintext)
            print("verified. proceeding...")
            processData(plaintext, passwords)
        else:
            print("Key incorrect or message corrupted")
            sg.Popup("Key incorrect or message corrupted. Exiting")
    #if files doesn't exist, proceed with empty string
    else:
        processData("", passwords)
        PasswordsManager(sg, passwords)

def processData(data,passwords):
    pass

def PasswordsManager(sg, passwords):
    #process data. format is website;email;password
    class Password:
        name: str
        email: str
        password: str
    # for line in tempfd:
    #     #create temp password
    #     temp = Password()
    #     #seperate the clauses
    #     #set attributes
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('This is your password')],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
    window = sg.Window('Password Manager', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
    window.close()