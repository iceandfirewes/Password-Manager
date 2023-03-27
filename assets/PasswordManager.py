import os
import pyperclip
from .EncryptDecrypt import encrypt, decrypt, getMetadata
from .Conversion import plainTextToPasswords, passwordsToPlainText, Password
def PasswordsManager(sg, passwords, hashedKey):
    # print(passwords[0].__str__())
    sg.theme('DarkAmber')   # Add a touch of color
    #table
    toprow =  ["Name","Username","Password","Comment"]
    rows = list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords))
    passwordsTable = sg.Table(values=rows, headings=toprow,
    auto_size_columns=False,
    display_row_numbers=False,
    justification='center', key='-passwordTable-',
    selected_row_colors=('#112A46','#ACC8E5'),
    enable_events=True,
    expand_x=True,
    expand_y=True,
    enable_click_events=True)
    layout = [  [passwordsTable],
                [sg.Column([[sg.Button('Add'), sg.Button('Edit'), sg.Button('Delete'), sg.Button("Save"), sg.Button('Exit'), sg.Button("Copy To Clipboard")]],justification='center')]]
    window = sg.Window('Password Manager', layout, size=(1000, 300))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        #DEBUG
        # print(f"""event: {event}\nvalues:{values}""")
        
        #handle table interaction
        #event: ('-passwordTable-', '+CLICKED+', (0, 1)) values: {'-passwordTable-': [1]}
        # if "+CLICKED+" in event:
        #     pass
        #get input, create, set attribute, append and update
        if event == "Add":
            #invoke passworkRequestForm(sg), assign return to tempFields. if not None then proceed
            if (tempFields := passwordRequestForm(sg))  != None:
            # tempFields = passwordRequestForm(sg)
            # #if user cancel the form
            # if(tempFields != None):
                tempPassword = Password()
                setattr(tempPassword, "name", tempFields["name"])
                setattr(tempPassword, "username", tempFields["username"])
                setattr(tempPassword, "password", tempFields["password"])
                setattr(tempPassword, "comment", tempFields["comment"])
                passwords.append(tempPassword)
                window["-passwordTable-"].update(list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords)))
        #example values -> values:{'-passwordTable-': [0]}
        #get input, create temp, set attribute, override and update
        elif event == "Edit":
            if(values["-passwordTable-"] != []):
                #invoke passworkRequestForm(), assign return to tempFields. if not None then proceed
                if (tempFields := passwordRequestForm(sg, passwords[values["-passwordTable-"][0]]))  != None:
                    selectedPasswordIndex = values["-passwordTable-"][0]
                    tempPassword = Password()
                    setattr(tempPassword, "name", tempFields["name"])
                    setattr(tempPassword, "username", tempFields["username"])
                    setattr(tempPassword, "password", tempFields["password"])
                    setattr(tempPassword, "comment", tempFields["comment"])
                    passwords[selectedPasswordIndex] = tempPassword
                    window["-passwordTable-"].update(list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords)))
        #example values -> values:{'-passwordTable-': [0]}
        elif event == "Delete":
            if(values["-passwordTable-"] != []):
                ch = sg.popup_yes_no("Are you sure?",  title="Password Deletion")
                if ch == "Yes":
                    passwords.pop(values["-passwordTable-"][0])
                    window["-passwordTable-"].update(list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords)))
        elif event == "Save":
            temp = passwordsToPlainText(passwords)
            encrypt(hashedKey, temp)
        elif event == sg.WIN_CLOSED or event == 'Exit':
            if(len(passwords)):
                temp = passwordsToPlainText(passwords)
                #DEBUG
                # print(temp)
                encrypt(hashedKey, temp)
            #if there is no passwords, just delete both .dat file
            else:
                if os.path.exists("passwordManagerData.dat"):
                    os.remove("passwordManagerData.dat")
                if os.path.exists("passwordManagerMetadata.dat"):
                    os.remove("passwordManagerMetadata.dat")
            break
        elif event == "Copy To Clipboard":
            plain = passwordsToPlainText(passwords)
            plain = plain.replace("\x1d","")
            plain = plain.replace("\x1e"," ")
            plain = plain.replace("\x1f"," ")
            pyperclip.copy(plain)
    window.close()
def verify(sg, hashedKey):
    passwords = []
    #if files exists, verifying
    if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
        #read the metadata and the ciphertext
        print("files exists. verifying...")
        nonce,tag  = getMetadata()
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
            sg.Popup("Key incorrect or data corrupted. Exiting")
    #if files doesn't exist, proceed with empty string
    elif (not os.path.isfile("passwordManagerData.dat")) and (not os.path.isfile("passwordManagerMetadata.dat")):
        plainTextToPasswords("", passwords)
        PasswordsManager(sg, passwords, hashedKey)
    else:
        sg.Popup("One of the .data file is missing. Please supply them or delete both passwordManagerData.data and passwordManagerMetadata.dat to reset.")
def passwordRequestForm(sg, password=None):
    layout = [  [sg.Text("Name"), sg.Push(), sg.InputText(default_text="" if password == None else password.name, key="name", size=20)],
                [sg.Text("Username"), sg.Push(), sg.InputText(default_text="" if password == None else password.username,key="username", size=20)],
                [sg.Text("Password"), sg.Push(), sg.InputText(default_text="" if password == None else password.password,key="password", size=20)],
                [sg.Text("Comment"), sg.Push(), sg.InputText(default_text="" if password == None else password.comment, key="comment", size=20)],
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