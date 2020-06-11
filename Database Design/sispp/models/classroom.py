class Classroom:
    def __init__(self, id, name, building, type, restoration_date, cap, conditioner="FALSE", board_type="Mixed"):
        self.id =id
        self.name = name
        self.building = building
        self.type = type
        self.restoration_date = restoration_date
        self.cap = cap
        self.conditioner = conditioner
        self.board_type = board_type

    def __str__(self):
    	return self.name + " - " + self.building + " " + self.type
