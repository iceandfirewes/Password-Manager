from .PasswordManager import PasswordManager

import hashlib
import os
def entryForm(sg, flagNewUser):
    info = """Please create a master key. Make sure that it is long and easy to remember.
Although, SHA256 hash is nearly impossible to crack, if you choose a simple key such as password.
Someone that has hashed the word password through SHA256 will know what the pre-hash key is."""
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  
                [sg.Text(info)],
                [sg.Text(f"Please {'create' if flagNewUser else 'enter'} your master key"), sg.InputText(key="input--key")],
                [sg.Button('Create'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window('Sign In' if flagNewUser else 'Log In', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'Create': # if user enter the master key
            window.close()
            #create the hashed key
            hashedKey = hashlib.sha256(str.encode(values["input--key"])).digest()
            PasswordManager(sg, hashedKey)
            break
        elif event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
    window.close()