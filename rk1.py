class Faculty:
    def __init__(self, id, name, university_id, student_count):
        self.id = id
        self.name = name
        self.university_id = university_id
        self.student_count = student_count

class University:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class FacultyUniversity:
    def __init__(self, faculty_id, university_id):
        self.faculty_id = faculty_id
        self.university_id = university_id

universities = [
    University(1, "МГТУ"),
    University(2, "СПбГУ"),
    University(3, "МГУ")
]

faculties = [
    Faculty(1, "Филологический", 1, 300),
    Faculty(2, "Математический", 1, 250),
    Faculty(3, "Экономический", 2, 200),
    Faculty(4, "Юридический", 3, 150),
    Faculty(5, "Биологический", 3, 180)
]

faculty_universities = [
    FacultyUniversity(1, 1),
    FacultyUniversity(2, 1),
    FacultyUniversity(3, 2),
    FacultyUniversity(4, 3),
    FacultyUniversity(5, 3),
    FacultyUniversity(1, 2),
    FacultyUniversity(3, 3)
]

def main():
    print("Запрос 1: Список университетов и их факультетов (сортировка по университету):")
    university_faculties = {}
    for faculty in faculties:
        university_id = faculty.university_id
        university = next(u for u in universities if u.id == university_id)
        if university.name not in university_faculties:
            university_faculties[university.name] = []
        university_faculties[university.name].append(faculty.name)

    for university_name in sorted(university_faculties.keys()):
        faculties_list = university_faculties[university_name]
        print(f"{university_name}: {', '.join(sorted(faculties_list))}")

    print("\nЗапрос 2: Количество факультетов по университетам (сортировка по количеству):")
    faculty_count = {}
    for f in faculty_universities:
        faculty_count[f.university_id] = faculty_count.get(f.university_id, 0) + 1
    result2 = sorted(
        [(next(u.name for u in universities if u.id == uid), count)
         for uid, count in faculty_count.items()],
        key=lambda x: x[1]
    )
    for university_name, count in result2:
        print(f"{university_name}: {count}")

    print("\nЗапрос 3: Факультеты на 'ий' и их университеты:")
    result3 = [
        (f.name, [u.name for u in universities
                  if any(fu.university_id == u.id and fu.faculty_id == f.id
                         for fu in faculty_universities)])
        for f in faculties if f.name.endswith("ий")
    ]
    for faculty_name, university_list in result3:
        print(f"{faculty_name}: {', '.join(university_list)}")

if __name__ == "__main__":
    main()
