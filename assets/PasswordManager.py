import os
from .EncryptDecrypt import encrypt, decrypt, returnMetadata
from .Conversion import plainTextToPasswords, passwordsToPlainText, Password
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
    layout = [  [passwordsTable],
                [sg.Button('Add'), sg.Button('Edit'), sg.Button('Delete'), sg.Button("Save"), sg.Button('Exit')] ]
    window = sg.Window('Password Manager', layout, size=(1000, 300))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        #DEBUG
        # print(f"""event: {event}\nvalues:{values}""")
        if event == sg.WIN_CLOSED or event == 'Exit':
            temp = passwordsToPlainText(passwords)
            #DEBUG
            # print(temp)
            encrypt(hashedKey, temp)
            break
        #handle table interaction
        #event: ('-passwordTable-', '+CLICKED+', (0, 1)) values: {'-passwordTable-': [1]}
        # if "+CLICKED+" in event:
        #     pass
        #get input, create, set attribute, append and update
        if event == "Add":
            tempFields = passwordRequestForm(sg)
            #if user cancel the form
            if(tempFields != None):
                tempPassword = Password()
                setattr(tempPassword, "name", tempFields["name"])
                setattr(tempPassword, "username", tempFields["username"])
                setattr(tempPassword, "password", tempFields["password"])
                setattr(tempPassword, "comment", tempFields["comment"])
                passwords.append(tempPassword)
                window["-passwordTable-"].update(list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords)))
        #example values -> values:{'-passwordTable-': [0]}
        #get input, create temp, set attribute, override and update
        if event == "Edit":
            if(values["-passwordTable-"] != []):
                tempFields = passwordRequestForm(sg, passwords[values["-passwordTable-"][0]])
                #if user cancel the form
                if(tempFields != None):
                    selectedPasswordIndex = values["-passwordTable-"][0]
                    tempPassword = Password()
                    setattr(tempPassword, "name", tempFields["name"])
                    setattr(tempPassword, "username", tempFields["username"])
                    setattr(tempPassword, "password", tempFields["password"])
                    setattr(tempPassword, "comment", tempFields["comment"])
                    passwords[selectedPasswordIndex] = tempPassword
                    window["-passwordTable-"].update(list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords)))
        #example values -> values:{'-passwordTable-': [0]}
        if event == "Delete":
            if(values["-passwordTable-"] != []):
                ch = sg.popup_yes_no("Are you sure?",  title="Password Deletion")
                if ch == "Yes":
                    passwords.pop(values["-passwordTable-"][0])
                    window["-passwordTable-"].update(list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords)))
        if event == "Save":
            temp = passwordsToPlainText(passwords)
            encrypt(hashedKey, temp)
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
            #DEBUG
            # print("The message is authentic:", plaintext)
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
def passwordRequestForm(sg, password=None):
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
            if (values["name"] and values["username"] and values["password"]):
                window.close()
                return {"name":values["name"], "username":values["username"], "password":values["password"], "comment":values["comment"]}
            else:
                sg.popup_auto_close("name/username/password need to be filled")
    window.close()