import os
from .EncryptDecrypt import encrypt, decrypt
from .Conversion import plainTextToPasswords, passwordsToPlainText
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
            plainTextToPasswords(plaintext.decode("utf-8"), passwords)
            PasswordsManager(sg, passwords, hashedKey)
        else:
            print("Key incorrect or message corrupted")
            sg.Popup("Key incorrect or message corrupted. Exiting")
    #if files doesn't exist, proceed with empty string
    else:
        plainTextToPasswords("", passwords)
        PasswordsManager(sg, passwords, hashedKey)
def PasswordsManager(sg, passwords, hashedKey):

    # print(passwords[0].__str__())
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('This is your password')],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
    window = sg.Window('Password Manager', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            temp = passwordsToPlainText(passwords)
            #DEBUG
            print(temp)
            encrypt(hashedKey, temp)
            break
    window.close()