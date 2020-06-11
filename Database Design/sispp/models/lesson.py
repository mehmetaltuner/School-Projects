class Lesson:
	def __init__(self, crn, date, code, instructor, location, assistant, credit, cap=0, enrolled=0, id=None):
		self.id = id
		self.crn = crn
		self.date = date
		self.code = code
		self.instructor = instructor
		self.location = location
		self.assistant = assistant
		self.credit = credit
		self.cap = cap
		self.enrolled = enrolled
