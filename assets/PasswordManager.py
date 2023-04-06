import os
import pyperclip
from .EncryptDecrypt import encrypt, decrypt, getMetadata
from .Conversion import plaintextToJSON, JSONToPlaintext, Password
from .ImportExport import exportJSON, importJSON
import csv
version = "1.3.0"
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
            print(type(data["passwords"]))
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
    sg.theme('DarkAmber')   # Add a touch of color
    #table
    print(type(passwords))
    toprow =  ["ID","Name","Username","Password","Comment"]
    rows = list(map(lambda password:  [password.id, password.name, password.username, password.password, password.comment], passwords))
    # rows = list(map(lambda password: [password["id"], password["name"], password["username"], password["password"], password["comment"]], passwords))
    
    # toprow =  ["ID","Name","Username","Password","Comment"]
    # rows = [[index, password.name, password.username, password.password, password.comment] for index,password in enumerate(passwords)]
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
                [sg.Text("Hotkey", tooltip=hotkeyTooltip)],
                [passwordsTable],
                [sg.Column([[sg.Button('Add'), sg.Button('E̲dit', key='Edit'), sg.Button('D̲elete', key='Delete'), sg.Button("S̲ave", key='Save'), sg.Button('Ex̲it', key='Exit'), sg.Button("Copy To Clipboard"), sg.Button("Import CSV")]],justification='center')]]
    return sg.Window('Password Manager', layout, size=(1000, 300), finalize=True)

def updateTable(window, passwords, selectIndex=None):
    window["-passwordTable-"].update(list(map(lambda password: [password.id, password.name, password.username, password.password, password.comment], passwords)))
    # window["-passwordTable-"].update(list(map(lambda password: [password["id"], password["name"], password["username"], password["password"], password["comment"]], passwords)))
    #if a row index is given, select it
    if(selectIndex != None):
        window["-passwordTable-"].update(select_rows=[selectIndex])
def programLoop(sg, window, passwords, hashedKey):
    global data
    global version
    while True:
        event, values = window.read()
        #DEBUG
        # print(f"""event: {event}\nvalues:{values}""")
        # if "+CLICKED+" in event:
        #     print(f"""event: {event}\nvalues:{values}""")
        #get input, create, set attribute, append and update
        #MAIN MENU
        if event == "Add":
            #invoke passworkRequestForm(sg), assign return to tempFields. if not None then proceed
            if (tempFields := passwordRequestForm(sg))  != None:
            # tempFields = passwordRequestForm(sg)
            # #if user cancel the form
            # if(tempFields != None):
                tempPassword = Password(len(passwords), tempFields["name"], tempFields["username"], tempFields["password"], tempFields["comment"])
                passwords.append(tempPassword)
                updateTable(window, passwords, len(passwords) - 1)
                print(type(passwords))
                # window["-passwordTable-"].update(list(map(lambda password:  [password.name, password.username, password.password, password.comment], passwords)),select_rows=None)
            window.write_event_value(("-passwordTable-","+CLICKED+",(0,0)), [0])
            # window.write_event_value("-passwordTable-", [0])
        #example values -> values:{'-passwordTable-': [0]}
        #get input, create temp, set attribute, override and update
        elif event == "Edit":
            if(values["-passwordTable-"] != []):
                #invoke passworkRequestForm(), assign return to tempFields. if not None then proceed
                if (tempFields := passwordRequestForm(sg, passwords[values["-passwordTable-"][0]]))  != None:
                    selectedPasswordIndex = values["-passwordTable-"][0]
                    tempPassword = Password(passwords[selectedPasswordIndex].id, tempFields["name"], tempFields["username"], tempFields["password"], tempFields["comment"])
                    passwords[selectedPasswordIndex] = tempPassword
                    updateTable(window, passwords, selectedPasswordIndex)
        elif event == "Delete":
            passwordDeleteForm(sg, window, values, passwords)
        elif event == "Save":
            #DEBUG
            tempPassword = Password()
            setattr(tempPassword, "id", 0)
            setattr(tempPassword, "name", "a")
            setattr(tempPassword, "username", "b")
            setattr(tempPassword, "password", "c")
            setattr(tempPassword, "comment", "d")
            data["passwords"].append(tempPassword)
            
            encrypt(hashedKey, JSONToPlaintext(data,version))
        elif event == sg.WIN_CLOSED or event == 'Exit':
            if(len(passwords)):
                temp = JSONToPlaintext(passwords)
                #DEBUG
                # print(temp)
                encrypt(hashedKey, temp)
            #if there is no passwords created, just delete both .dat file
            else:
                if os.path.exists("passwordManagerData.dat"):
                    os.remove("passwordManagerData.dat")
                if os.path.exists("passwordManagerMetadata.dat"):
                    os.remove("passwordManagerMetadata.dat")
            break
        elif event == "Copy To Clipboard":
            plain = passwordsToPlainText(passwords, version)
            plain = plain.replace("\x1d","")
            plain = plain.replace("\x1e"," ")
            plain = plain.replace("\x1f"," ")
            pyperclip.copy(plain)
        elif event == "Import CSV":
            csvRequestForm(sg, window, passwords)
        #TASKBAR
        elif event == "Export as JSON":
            exportJSON(sg, passwords)
        elif event == "Import from JSON":
            importJSON(sg, window, passwords)
    window.close()

def passwordRequestForm(sg, password=None):
    layout = [  [sg.Text("Name and Password is the minimum")],
                [sg.Text("Name"), sg.Push(), sg.InputText(default_text="" if password == None else password.name, key="name", size=20)],
                [sg.Text("Username"), sg.Push(), sg.InputText(default_text="" if password == None else password.username,key="username", size=20)],
                [sg.Text("Password"), sg.Push(), sg.InputText(default_text="" if password == None else password.password,key="password", size=20)],
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
        if event == "Enter":
            #input validation
            if (values["name"] and values["password"]):
                window.close()
                return {"name":values["name"], "username":values["username"], "password":values["password"], "comment":values["comment"]}
            else:
                sg.popup_auto_close("name/password need to be filled")
    window.close()

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
                passwords.pop(rootValues["-passwordTable-"][0])
                updateTable(rootWindow, passwords)
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
                            tempPassword = Password()
                            setattr(tempPassword, "name", row[0])
                            setattr(tempPassword, "username", row[1])
                            setattr(tempPassword, "password", row[2])
                            setattr(tempPassword, "comment", row[3])
                            passwords.append(tempPassword)
                    updateTable(rootWindow, passwords)
                    csvWindow.close()
                    return
    csvWindow.close()