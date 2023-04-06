import json
class Password:
    id: int
    name: str
    username: str
    password: str
    comment: str
    def __init__(self, id, name, username, password, comment):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.comment = comment
    def __str__(self):
        return (f"""name:{self.name};username:{self.username};password:{self.password};comment:{self.comment}""")
    class CustomEncoder(json.JSONEncoder):
        def default(self, o):
                return o.__dict__

def plaintextToJSON(text,version):
    if(text == ""):
        return {"passwords":[],"version":version}
    else:
        data = json.loads(text)
        passwords = data["passwords"]
        data["passwords"] = list(map(lambda password:  Password(password["id"], password["name"], password["username"], password["password"], password["comment"]), passwords))
        return data
        # #FIX THIS
        # for line in data.split("\x1d\n"):
        #     if line != "":
        #         password = Password()
        #         for clause in line.split("\x1e"):
        #             nameValuePair = clause.split("\x1f")
        #             #DEBUG
        #             #print(nameValuePair)
        #             setattr(password,nameValuePair[0],nameValuePair[1])
        #         data["passwords"].append(password)
    # return passwords
def JSONToPasswords(data, passwords):
    data = json.loads(data)
    print(data)
def JSONToPlaintext(data,version):
    newdata = {
        "passwords":data["passwords"],
        "version":version
    }
    return json.dumps(newdata,cls=Password.CustomEncoder)
    # passwordJSONString = list(map(lambda password: password.toJSON(), data["passwords"]))
    # print(passwordJSONString)
    # jsonString = f'''{{"password":{data["password"]}}}'''
    # print(jsonString)
    # return json.dumps(data["passwords"][0])
    # plainTextList = []
    # for password in passwords:
    #     temp = password.__dict__
    #     plainTextList.append(f"""name\x1f{temp["name"]}\x1eusername\x1f{temp["username"]}\x1epassword\x1f{temp["password"]}\x1ecomment\x1f{temp["comment"]}""")
    # return '\x1d\n'.join(plainTextList)