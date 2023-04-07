import json
from .Conversion import Password
def exportJSON(sg, passwords, version):
    passwordsObj = {
                "passwords":list(
                    map(lambda password: 
                        {
                            "id": password.id,
                            "name":password.name, 
                            "username":password.username, 
                            "password":password.password, 
                            "comment":password.comment}, passwords)),
                "version":version
                        }
    with open("passwordManagerRawData.json","w") as fd:
        fd.write(json.dumps(passwordsObj, indent=4))
        fd.close()
    sg.popup_auto_close("json file has been created. Please make sure to delete it after use.")
#NOT DONE
def importJSON(sg,rootWindow, passwords):
    layout = [
        [sg.Text("Please select a JSON file")],
        [sg.InputText(key="path"), sg.FileBrowse(file_types=[("JSON File","*.json")])],
        [sg.Button("Ok"), sg.Button("Cancel")]
    ]
    jsonWindow = sg.Window('File Selector', layout, finalize=True, modal=True)
    jsonWindow.bind('<Escape>','Cancel')
    while True:
        eventJSON, valuesJSON = jsonWindow.read()
        #DEBUG
        # valuesJSON[""] = "C:/Users/icean/Downloads/projects/Password-Manager/PasswordManagerRawData.json"
        # jsonWindow["Ok"].click()
        # jsonWindow.close()
        # break
        # print(f"""event: {eventJSON}\nvalue:{valuesJSON}""")
        if(eventJSON == sg.WIN_CLOSED or eventJSON == 'Cancel'):
            break
        elif(eventJSON == "Ok"):
            if(valuesJSON["path"]):
                with open(valuesJSON["path"]) as jsonFD:
                    data = json.load(jsonFD)
                    # print(data)
                    #import 1.2. add version
                    if("version" not in data):
                        data["version"] = "1.3.0"
                    print(data)
                    #maybe swap to version file first
                    # KEEP WORKING ON THIS. NEED TO make a passwords list
    jsonWindow.close()