from .people import People


class Student(People):
    def __init__(self, name, number, mail, cred, depart, facu, club=None, lab=None, password=None, photo=None):
        self.name = name
        self.number = number
        self.mail = mail
        self.cred = cred
        self.depart = depart
        self.facu = facu
        self.club = club
        self.lab = lab
        self.password = password
        self.photo = photo

        if not self.club:
            self.club = None

        if not self.lab:
            self.lab = None

    def get_person_obj(self):
    	return People(name = self.name, mail = self.mail, password=self.password, photo=self.photo, type="student")
