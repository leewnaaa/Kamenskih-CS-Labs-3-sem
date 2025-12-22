from data import get_universities, get_faculties, get_faculty_universities
from queries import get_university_faculties, get_faculty_count, get_faculties_ending_with_iy

def main():
    universities = get_universities()
    faculties = get_faculties()
    faculty_universities = get_faculty_universities()

    print("Запрос 1: Список университетов и их факультетов (сортировка по университету):")
    result1 = get_university_faculties(universities, faculties)
    for university_name, faculties_list in result1.items():
        print(f"{university_name}: {', '.join(faculties_list)}")

    print("\nЗапрос 2: Количество факультетов по университетам (сортировка по количеству):")
    result2 = get_faculty_count(universities, faculty_universities)
    for university_name, count in result2:
        print(f"{university_name}: {count}")

    print("\nЗапрос 3: Факультеты на 'ий' и их университеты:")
    result3 = get_faculties_ending_with_iy(faculties, universities, faculty_universities)
    for faculty_name, university_list in result3:
        print(f"{faculty_name}: {', '.join(university_list)}")

if __name__ == "__main__":
    main()
