import os.path
from Crypto.Cipher import AES 
def verify(sg, hashedKey):
    #check integrity of nonce and dat
    if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
        print("password file exists. verifying...")
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
            print("verified. proceeding...")
            #temp file creation
            fd = open("~$passwordManagerData.dat","w")
            fd.write(plaintext.decode("utf-8"))
            fd.close()
            fd = open("~$passwordManagerData.dat","r")
            PasswordsManager(sg, fd)
            fd.close()
            #print("The message is authentic:", plaintext)
        except ValueError:
            print("Key incorrect or message corrupted")
            sg.Popup("Key incorrect or message corrupted. Exiting")
            return
    #if file doesnt exist
    else:
        #temp file creation
        fd = open("~$passwordManagerData.dat","x")
        fd.close()
        fd = open("~$passwordManagerData.dat","r") 
        PasswordsManager(sg, fd)
        fd.close()

def PasswordsManager(sg, fd):
    #process data. format is website;email;password
    class Password:
        name: str
        email: str
        password: str
    for line in fd:
        #create temp password
        temp = Password()
        #seperate the clauses
        #set attributes
        print(line)
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