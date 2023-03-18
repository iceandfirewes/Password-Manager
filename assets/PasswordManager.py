import os
from .EncryptDecrypt import encrypt, decrypt, returnMetadata
from .Conversion import plainTextToPasswords, passwordsToPlainText
def PasswordsManager(sg, passwords, hashedKey):
    # print(passwords[0].__str__())
    sg.theme('DarkAmber')   # Add a touch of color
    #table
    toprow =  ["Name","Username","Password","Comment"]
    rows = list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords))
    passwordsTable = sg.Table(values=rows, headings=toprow,
    auto_size_columns=True,
    display_row_numbers=False,
    justification='center', key='-passwordTable-',
    selected_row_colors='red on yellow',
    enable_events=True,
    expand_x=True,
    expand_y=True,
    enable_click_events=True)
    # All the stuff inside your window.
    layout = [  [passwordsTable],
                [sg.Button('Add'), sg.Button('Edit'), sg.Button('Delete'), sg.Button('Cancel')] ]
    window = sg.Window('Password Manager', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print(f"""event: {event}\nvalues:{values}""")
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            temp = passwordsToPlainText(passwords)
            #DEBUG
            print(temp)
            encrypt(hashedKey, temp)
            break
        #handle table interaction
        #event: ('-passwordTable-', '+CLICKED+', (0, 1)) values: {'-passwordTable-': [1]}
        if "+CLICKED+" in event:
            # print(f"""You clicked row:{event[2][0]} Column: {event[2][1]}""")
            pass
        if event == "Add":
            temp = passwordRequestForm(sg, None)
            #append and update
            pass
        #value:{'-passwordTable-': [0]}
        if event == "Edit":
            if(values["-passwordTable-"] != []):
                temp = passwordRequestForm(sg, passwords[values["-passwordTable-"][0]])
                print(temp)
                #update passwords and table
            pass
        if event == "Delete":
            if(values["-passwordTable-"] != []):
                ch = sg.popup_yes_no("Are you sure?",  title="Password Deletion")
                if ch == "Yes":
                    print("deleted")
            pass
    window.close()
def verify(sg, hashedKey):
    passwords = []
    #if files exists, verifying
    if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
        #read the metadata and the ciphertext
        print("password file exists. verifying...")
        nonce,tag  = returnMetadata()
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
def passwordRequestForm(sg, password):
    layout = [  [sg.Text("Name"),sg.InputText(default_text="" if password == None else password.name, key="name")],
                [sg.Text("Username"),sg.InputText(default_text="" if password == None else password.username,key="username")],
                [sg.Text("Password"),sg.InputText(default_text="" if password == None else password.password,key="password")],
                [sg.Text("Comment"),sg.InputText(default_text="" if password == None else password.comment, key="comment")],
                [sg.Button("Ok")] ]
    window = sg.Window("Password Form", layout, modal=True)
    while True:
        event, values = window.read()
        #DEBUG
        # print(f"""event: {event}\nvalue:{values}""")
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Ok":
            #input validation
            window.close()
            return [values["name"], values["username"], values["password"], values["comment"]]
    window.close()