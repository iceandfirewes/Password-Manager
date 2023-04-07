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
def JSONToPasswords(data, passwords):
    data = json.loads(data)
    print(data)
def JSONToPlaintext(data,version):
    newdata = {
        "passwords":data["passwords"],
        "version":version
    }
    return json.dumps(newdata,cls=Password.CustomEncoder)