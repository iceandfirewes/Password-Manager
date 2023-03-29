from .PasswordManager import verify
import os
import hashlib
import textwrap
def entryForm(sg, flagNewUser):
    info = f"""Please create a master key. Make sure that it is long and easy to remember.
Although, SHA256 hash is nearly impossible to crack, if you choose a simple key such as password.
Someone that has hashed the word password through SHA256 will know what the pre-hash key is.
Please chose your password carefully as it cannot be changed without deleting all passwords stored""" if flagNewUser else "Welcome"
    # info = f"""Please create a master key. Make sure that it is long and easy to remember. Although, SHA256 hash is nearly impossible to crack, if you choose a simple key such as password. Someone that has hashed the word password through SHA256 will know what the pre-hash key is. Please""" if flagNewUser else """Welcome"""
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  
                [sg.Text(textwrap.TextWrapper(width=50).fill(text=info))],
                [sg.Text(f"Please {'create' if flagNewUser else 'enter'} your master key"), sg.InputText(key="input--key", size=20)],
                [sg.Button('Sign in' if flagNewUser else 'Log in',key="input--enter"), sg.Button('Cancel'),sg.Push(), sg.Button('Reset')]  ]

    # Create the Window
    window = sg.Window('Sign In' if flagNewUser else 'Log In', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    # DEBUG
    # hashedKey = hashlib.sha256(str.encode("a")).digest()
    # verify(sg, hashedKey)
    # window.close()
    ###################
    while True:
        event, values = window.read()
        if event == 'input--enter':
            if(values["input--key"]):
                window.close()
                #create the hashed key
                hashedKey = hashlib.sha256(str.encode(values["input--key"])).digest()
                verify(sg, hashedKey)
                break
        elif event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == "Reset":
            ch = sg.popup_yes_no("Are you sure? This will delete all your passwords.",  title="Reset")
            if ch == "Yes":
                ch = sg.popup_yes_no("Are you doubly sure?",  title="Reset")
                if ch == "Yes":
                    if os.path.exists("passwordManagerData.dat"):
                        os.remove("passwordManagerData.dat")
                    if os.path.exists("passwordManagerMetadata.dat"):
                        os.remove("passwordManagerMetadata.dat")
                    sg.Popup("Please relaunch the application.")
                    break
    window.close()