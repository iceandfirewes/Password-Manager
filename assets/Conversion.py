def plainTextToPasswords(data, passwords):
    class Password:
        name: str
        email: str
        password: str
        def __str__(self):
            return (f"name:{self.name} email:{self.email} password:{self.password}")
    if(data == ""):
        pass
    else:
        for line in data.splitlines():
            if line != "":
                password = Password()
                for clause in line.split(";"):
                    nameValuePair = clause.split(":")
                    setattr(password,nameValuePair[0],nameValuePair[1])
                passwords.append(password)
    return passwords
def passwordsToPlainText(passwords):
    plainTextList = []
    for password in passwords:
        temp = password.__dict__
        plainTextList.append(f"""name:{temp["name"]};email:{temp["name"]};password:{temp["name"]}""")
    return '\n'.join(plainTextList)