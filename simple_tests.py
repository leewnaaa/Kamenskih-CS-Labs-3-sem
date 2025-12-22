from models import University, Faculty, FacultyUniversity
from queries import get_university_faculties, get_faculty_count, get_faculties_ending_with_iy

def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 50)
    print("Запуск модульных тестов")
    print("=" * 50)

    universities = [
        University(1, "Тестовый Университет 1"),
        University(2, "Тестовый Университет 2")
    ]

    faculties = [
        Faculty(1, "Тестовый факультет", 1, 50),
        Faculty(2, "Другой факультет", 2, 60)
    ]

    faculty_universities = [
        FacultyUniversity(1, 1),
        FacultyUniversity(2, 2)
    ]

    # Тест 1
    print("\nТест 1: get_university_faculties")
    result1 = get_university_faculties(universities, faculties)
    print(f"Результат: {result1}")
    assert len(result1) == 2, "Должно быть 2 университета"
    print("Тест 1 пройден")

    # Тест 2
    print("\nТест 2: get_faculty_count")
    result2 = get_faculty_count(universities, faculty_universities)
    print(f"Результат: {result2}")
    assert len(result2) == 2, "Должно быть 2 записи"
    print("Тест 2 пройден")

    # Тест 3
    print("\nТест 3: get_faculties_ending_with_iy")
    faculties_with_iy = faculties + [Faculty(3, "Химический", 1, 70)]
    result3 = get_faculties_ending_with_iy(faculties_with_iy, universities, faculty_universities)
    print(f"Результат: {result3}")
    assert any("Химический" in item for item in result3), "Должен найти 'Химический'"
    print("Тест 3 пройден")

    print("\n" + "=" * 50)
    print("Все тесты успешно пройдены!")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()
