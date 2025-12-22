def get_university_faculties(universities, faculties):
    """Запрос 1: Список университетов и их факультетов"""
    university_faculties = {}
    for faculty in faculties:
        university_id = faculty.university_id
        university = next(u for u in universities if u.id == university_id)
        if university.name not in university_faculties:
            university_faculties[university.name] = []
        university_faculties[university.name].append(faculty.name)

    result = {}
    for university_name in sorted(university_faculties.keys()):
        result[university_name] = sorted(university_faculties[university_name])

    return result

def get_faculty_count(universities, faculty_universities):
    """Запрос 2: Количество факультетов по университетам"""
    faculty_count = {}
    for f in faculty_universities:
        faculty_count[f.university_id] = faculty_count.get(f.university_id, 0) + 1

    result = []
    for uid, count in faculty_count.items():
        university = next(u for u in universities if u.id == uid)
        result.append((university.name, count))

    return sorted(result, key=lambda x: x[1])

def get_faculties_ending_with_iy(faculties, universities, faculty_universities):
    """Запрос 3: Факультеты на 'ий' и их университеты"""
    result = []

    for faculty in faculties:
        if faculty.name.endswith("ий"):
            uni_list = []
            for fu in faculty_universities:
                if fu.faculty_id == faculty.id:
                    university = next(u for u in universities if u.id == fu.university_id)
                    uni_list.append(university.name)

            result.append((faculty.name, uni_list))

    return result
