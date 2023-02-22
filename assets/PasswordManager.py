import os.path
from Crypto.Cipher import AES 
def PasswordManager(sg, hashedKey):
    #check integrity of nonce and dat
    if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
        print("files exist. verifying...")
        fdMeta = open("passwordManagerMetadata.dat","rb")
        nonce = fdMeta.read(16)
        tag = fdMeta.read(16)
        print(f"nonce: {nonce} with {len(nonce)} length")
        print(f"tag: {tag} with {len(tag)} length")
        fdMeta.close()
        cipher = AES.new(hashedKey, AES.MODE_EAX, nonce=nonce)
        fd = open("passwordManagerData.dat","rb")
        ciphertext = fd.read()
        fd.close()
        plaintext = cipher.decrypt(ciphertext)
        print(plaintext)
        try:
            cipher.verify(tag)
            print("The message is authentic:", plaintext)
        except ValueError:
            print("Key incorrect or message corrupted")
    else:
        pass
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