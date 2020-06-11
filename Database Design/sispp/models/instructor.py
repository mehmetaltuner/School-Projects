class Instructor:
    def __init__(self, instructor_id, name, bachelors, masters, doctorates, department, room, lab=None):
        self.bachelors = bachelors
        self.masters = masters
        self.doctorates = doctorates
        self.instructor_id = instructor_id
        self.name = name
        self.department = department
        self.room = room
        self.lab = lab

        if not self.lab:
            self.lab = None
