class University:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Faculty:
    def __init__(self, id, name, university_id, student_count):
        self.id = id
        self.name = name
        self.university_id = university_id
        self.student_count = student_count

class FacultyUniversity:
    def __init__(self, faculty_id, university_id):
        self.faculty_id = faculty_id
        self.university_id = university_id
