class Password:
    name: str
    username: str
    password: str
    comment: str
    def __str__(self):
        return (f"""name:{self.name};username:{self.username};password:{self.password};comment:{self.comment}""")
def plainTextToPasswords(data, passwords):
    if(data == ""):
        pass
    else:
        for line in data.split("\x1d\n"):
            if line != "":
                password = Password()
                for clause in line.split("\x1e"):
                    nameValuePair = clause.split("\x1f")
                    #DEBUG
                    #print(nameValuePair)
                    setattr(password,nameValuePair[0],nameValuePair[1])
                passwords.append(password)
    return passwords
def passwordsToPlainText(passwords):
    plainTextList = []
    for password in passwords:
        temp = password.__dict__
        plainTextList.append(f"""name\x1f{temp["name"]}\x1eusername\x1f{temp["username"]}\x1epassword\x1f{temp["password"]}\x1ecomment\x1f{temp["comment"]}""")
    return '\x1d\n'.join(plainTextList)