import os.path
from Crypto.Cipher import AES 
def PasswordManager(sg, hashedKey):
    #check integrity of nonce and dat
    if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
        print("files exist. verifying...")
        fdMeta = open("passwordManagerMetadata.dat","rb")
        nonce = fdMeta.read(16)
        tag = fdMeta.read(16)
        fdMeta.close()
        fd = open("passwordManagerData.dat","rb")
        ciphertext = fd.read()
        fdMeta.close()
        cipher = AES.new(hashedKey, AES.MODE_EAX, nonce=nonce)
        fd.close()
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
            print("The message is authentic:", plaintext)
        except ValueError:
            print("Key incorrect or message corrupted")
            sg.Popup("Key incorrect or message corrupted. Exiting")
            return
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