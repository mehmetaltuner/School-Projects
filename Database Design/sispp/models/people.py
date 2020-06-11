import json

class People:
    def __init__(self, name, id=None, mail=None, photo=None, password=None, admin=False, type=None):
        self.name = name
        self.id = id
        self.mail = mail
        self.photo = photo
        self.password = password
        self.type = type
        self.admin = admin

    def toJSON(self):
	    return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)