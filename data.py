from models import University, Faculty, FacultyUniversity

def get_universities():
    return [
        University(1, "МГТУ"),
        University(2, "СПбГУ"),
        University(3, "МГУ")
    ]

def get_faculties():
    return [
        Faculty(1, "Филологический", 1, 300),
        Faculty(2, "Математический", 1, 250),
        Faculty(3, "Экономический", 2, 200),
        Faculty(4, "Юридический", 3, 150),
        Faculty(5, "Биологический", 3, 180)
    ]

def get_faculty_universities():
    return [
        FacultyUniversity(1, 1),
        FacultyUniversity(2, 1),
        FacultyUniversity(3, 2),
        FacultyUniversity(4, 3),
        FacultyUniversity(5, 3),
        FacultyUniversity(1, 2),
        FacultyUniversity(3, 3)
    ]
