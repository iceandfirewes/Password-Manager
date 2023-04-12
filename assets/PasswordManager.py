import os
import pyperclip
from .EncryptDecrypt import encrypt, decrypt
from .Conversion import plaintextToJSON, JSONToPlaintext, Password
from .ImportExport import exportJSON, importJSON
import csv
import random
version = "2.2.0"
data = None
def PasswordsManager(sg, passwords, hashedKey):
    window = initializeUI(sg, passwords)
    window.bind('<Control-c>',"Password Copy")
    window.bind('<Return>',"Add")
    window.bind('<Alt-e>',"Edit")
    window.bind('<Alt-d>',"Delete")
    window.bind('<Alt-s>',"Save")
    window.bind('<Alt-x>',"Exit")
    window.bind('<Escape>',"Exit")
    programLoop(sg, window, passwords, hashedKey)

def verify(sg, hashedKey):
    global data
    #if files exists, verifying
    if os.path.isfile("passwordManagerData.dat") & os.path.isfile("passwordManagerMetadata.dat"):
        #read the metadata and the ciphertext
        print("files exists. verifying...")
        if(plaintext := decrypt(hashedKey)):
            #DEBUG
            # print("The message is authentic:", plaintext)
            print("verified. proceeding...")
            data = plaintextToJSON(plaintext.decode("utf-8"), version)
            PasswordsManager(sg, data["passwords"], hashedKey)
        else:
            print("Key incorrect or message corrupted")
            sg.Popup("Key incorrect or data corrupted. Exiting")
    #if files doesn't exist, proceed with empty string
    elif (not os.path.isfile("passwordManagerData.dat")) and (not os.path.isfile("passwordManagerMetadata.dat")):
        data = plaintextToJSON("", version)
        PasswordsManager(sg, data["passwords"], hashedKey)
    else:
        sg.Popup("One of the .data file is missing. Please supply them or delete both passwordManagerData.data and passwordManagerMetadata.dat to reset.")

def initializeUI(sg, passwords):
    sg.theme('DarkAmber')
    #table
    toprow =  ["ID","Name","Username","Password","Comment"]
    rows = list(map(lambda password:  [password.id, password.name, password.username, password.password, password.comment], passwords))
    passwordsTable = sg.Table(values=rows, headings=toprow,
    auto_size_columns=False,
    display_row_numbers=False,
    justification='center', key='-passwordTable-',
    selected_row_colors=('#112A46','#ACC8E5'),
    enable_events=True,
    expand_x=True,
    expand_y=True,
    enable_click_events=True)
    #taskbar
    # menu_def = [['File', ['Export as JSON',"Import from JSON"]]]
    menu_def = [['File', ['Export as JSON']]]
    #layout
    hotkeyTooltip = f"""Enter - Add\nAlt+E/D/S/X\nCtrl+C - Copy Password\nESC - Exit Current Menu"""
    layout = [  [sg.Menu(menu_def)],
                [sg.Text("Name Search:"), sg.Input(enable_events=True, key="nameSearch"),sg.Push(), sg.Text("Hotkey", tooltip=hotkeyTooltip)],
                [passwordsTable],
                [sg.Column([[sg.Button('Add'), sg.Button('E̲dit', key='Edit'), sg.Button('D̲elete', key='Delete'), sg.Button("S̲ave", key='Save'), sg.Button('Ex̲it', key='Exit'), sg.Button("Copy To Clipboard"), sg.Button("Import CSV")]],justification='center')]]
    return sg.Window('Password Manager', layout, size=(1000, 300), finalize=True)

def updateTable(window, passwords, selectPassword=None, nameSearch=None):
    if nameSearch:
        #filter password so it only contain password that have nameSearch in them. then map over those passwords
        filteredPasswords = list(filter(lambda password: nameSearch in password.name ,passwords))
        window["-passwordTable-"].update(list(map(lambda password: [password.id, password.name, password.username, password.password, password.comment], filteredPasswords)))
    else:
        window["-passwordTable-"].update(list(map(lambda password: [password.id, password.name, password.username, password.password, password.comment], passwords)))
    # if(selectIndex != None):
    #     window["-passwordTable-"].update(select_rows=[selectIndex])
    if selectPassword != None:
        for index, password in enumerate(window["-passwordTable-"].Values):
            if password[0] == selectPassword.id:
                window["-passwordTable-"].update(select_rows=[index])
def programLoop(sg, window, passwords, hashedKey):
    global data
    # global version
    while True:
        event, values = window.read()
        #DEBUG
        # print(f"""event:{event}\nvalues:{values}""")
        # print(f"""table:{window["-passwordTable-"].Values}\n""")
        # if "+CLICKED+" in event:
        #     print(f"""event: {event}\nvalues:{values}""")
        #get input, create, set attribute, append and update
        #SEARCH
        if event == "nameSearch":
            updateTable(window, passwords, nameSearch=values["nameSearch"])
        #MAIN MENU
        elif event == "Add":
            passwordRequestForm(sg, window, passwords, values, "Add")
        elif event == "Edit":
            # if a row is selected
            if(values["-passwordTable-"] != []):
                selectedRow = values["-passwordTable-"][0]
                selectedPasswordID = window["-passwordTable-"].Values[selectedRow][0]
                passwordIndex = searchPasswordIndex(passwords, selectedPasswordID)
                passwordRequestForm(sg, window, passwords, values, "Edit", passwords[passwordIndex])
        elif event == "Delete":
            passwordDeleteForm(sg, window, values, passwords)
        elif event == "Save":
            print(len(window["-passwordTable-"].Values))
            encrypt(hashedKey, JSONToPlaintext(data,version))
        elif event == sg.WIN_CLOSED or event == 'Exit':
            if(len(passwords)):
                temp = JSONToPlaintext(data, version)
                encrypt(hashedKey, temp)
            #if there is no passwords created, just delete both .dat file
            else:
                if os.path.exists("passwordManagerData.dat"):
                    os.remove("passwordManagerData.dat")
                if os.path.exists("passwordManagerMetadata.dat"):
                    os.remove("passwordManagerMetadata.dat")
            break
        elif event == "Copy To Clipboard":
            def test(password):
                name = f"name:{password.name}" if password.name else None
                username = f"username:{password.username}" if password.username else None
                passwordP = f"password:{password.password}" if password.password else None
                comment = f"comment:{password.comment}" if password.comment else None
                password = [name,username,passwordP, comment]   
                return " ".join(filter(None,password))
            listPasswords = list(map(lambda password: test(password), passwords))
            pyperclip.copy("\n".join(listPasswords))
        elif event == "Import CSV":
            csvRequestForm(sg, window, passwords)
        #TASKBAR
        elif event == "Export as JSON":
            exportJSON(sg, passwords, version)
        elif event == "Import from JSON":
            importJSON(sg, window, passwords)
        #HOTKEY
        elif event == "Password Copy":
            if(values["-passwordTable-"] != []):
                selectedRow = values["-passwordTable-"][0]
                selectedPasswordID = window["-passwordTable-"].Values[selectedRow][0]
                pyperclip.copy(passwords[searchPasswordIndex(passwords, selectedPasswordID)].password)
    window.close()
#LEGACY psswordRequestForm
# def passwordRequestForm(sg, password=None):
#     layout = [  [sg.Text("Name and Password is the minimum")],
#                 [sg.Text("Name"), sg.Push(), sg.InputText(default_text="" if password == None else password.name, key="name", size=20)],
#                 [sg.Text("Username"), sg.Push(), sg.InputText(default_text="" if password == None else password.username,key="username", size=20)],
#                 [sg.Text("Password"), sg.Push(), sg.InputText(default_text="" if password == None else password.password,key="password", size=20)],
#                 [sg.Text("Comment"), sg.Push(), sg.InputText(default_text="" if password == None else password.comment, key="comment", size=20)],
#                 [sg.Button("Enter", bind_return_key=True)] ]
#     window = sg.Window("Password Form", layout, modal=True, finalize=True)
#     window.bind('<Return>',"Enter")
#     window.bind('<Escape>',"Exit")
#     while True:
#         event, values = window.read()
#         #DEBUG
#         # print(f"""event: {event}\nvalue:{values}""")
#         if event == "Exit" or event == sg.WIN_CLOSED:
#             break
#         if event == "Enter":
#             if (values["name"] and values["password"]):
#                 window.close()
#                 return {"name":values["name"], "username":values["username"], "password":values["password"], "comment":values["comment"]}
#             else:
#                 sg.popup_auto_close("name/password need to be filled")
#     window.close()
def passwordRequestForm(sg, rootWindow, passwords, rootValues, action, password=None):
    layout = [  [sg.Text("Name and Password is the minimum")],
            [sg.Text("Name"), sg.Push(), sg.InputText(default_text="" if password == None else password.name, key="name", size=20)],
            [sg.Text("Username"), sg.Push(), sg.InputText(default_text="" if password == None else password.username,key="username", size=20)],
            [sg.Text("Password"), sg.Button("Generate"), sg.InputText(default_text="" if password == None else password.password,key="password", size=20)],
            [sg.Text("Comment"), sg.Push(), sg.InputText(default_text="" if password == None else password.comment, key="comment", size=20)],
            [sg.Button("Enter", bind_return_key=True)] ]
    window = sg.Window("Password Form", layout, modal=True, finalize=True)
    window.bind('<Return>',"Enter")
    window.bind('<Escape>',"Exit")
    while True:
        event, values = window.read()
        #DEBUG
        # print(f"""event: {event}\nvalue:{values}""")
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Enter":
            if values["name"] and values["password"]:
                if action == "Add":
                    id = 0 if passwords[-1:] == [] else passwords[-1].id + 1
                    # updateTable(window, passwords, selectIndex=len(passwords) - 1)
                    tempPassword = Password(id, values["name"], values["username"], values["password"], values["comment"])
                    passwords.append(tempPassword)
                    updateTable(rootWindow, passwords, selectPassword=tempPassword,nameSearch=rootValues["nameSearch"])
                    break
                elif action == "Edit":
                    selectedRow = rootValues["-passwordTable-"][0]
                    selectedPasswordID = rootWindow["-passwordTable-"].Values[selectedRow][0]
                    passwordIndex = searchPasswordIndex(passwords, selectedPasswordID)
                    tempPassword = Password(selectedPasswordID, values["name"], values["username"], values["password"], values["comment"])
                    passwords[passwordIndex] = tempPassword
                    updateTable(rootWindow, passwords, selectPassword=tempPassword, nameSearch=rootValues["nameSearch"])
                    break
            else:
                sg.popup_auto_close("name/password need to be filled")
        elif event == "Generate":
            generatedPassword = ""
            allowableCharacter = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!()?[]`~;:#$%^&*+="
            for i in range(13):
                generatedPassword += random.choice(allowableCharacter)
            window["password"].update(generatedPassword)
        
    window.close()
def searchPasswordIndex(passwords, id):
    for index, password in enumerate(passwords):
        if id == password.id:
            return index
def passwordDeleteForm(sg, rootWindow, rootValues,passwords):
    if(rootValues["-passwordTable-"] != []):
        layout = [
            [sg.T('Do you sure you want to delete this password?')],
            [sg.Column([[sg.Yes(s=10), sg.No(s=10)]], justification='center')]
        ]
        deleteWindow = sg.Window('Confirmation',layout, finalize=True, modal=True)
        deleteWindow.bind('<Escape>','No')
        deleteWindow.bind('<Return>','Yes')
        while True:
            eventDelete, valuesDelete = deleteWindow.read()
            if(eventDelete == sg.WIN_CLOSED or eventDelete == 'No'):
                break
            if(eventDelete == "Yes"):
                selectedRow = rootValues["-passwordTable-"][0]
                selectedPasswordID = rootWindow["-passwordTable-"].Values[selectedRow][0]
                passwords.pop(searchPasswordIndex(passwords, selectedPasswordID))
                updateTable(rootWindow, passwords, nameSearch=rootValues["nameSearch"])
                deleteWindow.close()
                return
        deleteWindow.close()
def csvRequestForm(sg,rootWindow, passwords):
    layout = [
        [sg.Text("Please select a csv file(name,username,password,comment)")],
        [sg.InputText(key="path"), sg.FileBrowse(file_types=[("CSV File","*.csv")])],
        [sg.Button("Ok"), sg.Button("Cancel")]
    ]
    csvWindow = sg.Window('File Selector', layout, finalize=True, modal=True)
    csvWindow.bind('<Escape>','Cancel')
    while True:
        eventCSV, valuesCSV = csvWindow.read()
        if(eventCSV == sg.WIN_CLOSED or eventCSV == 'Cancel'):
            break
        elif(eventCSV == "Ok"):
            if(valuesCSV["path"]):
                with open(valuesCSV["path"]) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for index,row in enumerate(csv_reader):
                        if(index):
                            tempPassword = Password(len(passwords),row[0], row[1], row[2], row[3])
                            passwords.append(tempPassword)
                    updateTable(rootWindow, passwords)
                    csvWindow.close()
                    return
    csvWindow.close()