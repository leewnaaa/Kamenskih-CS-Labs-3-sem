import pytest
from models import University, Faculty, FacultyUniversity
from queries import get_university_faculties, get_faculty_count, get_faculties_ending_with_iy

class TestUniversityQueries:
    """Тесты для функций запросов"""

    def setup_method(self):
        """Подготовка тестовых данных"""
        self.universities = [
            University(1, "Университет А"),
            University(2, "Университет Б")
        ]

        self.faculties = [
            Faculty(1, "Филологический", 1, 100),
            Faculty(2, "Математический", 1, 150),
            Faculty(3, "Экономический", 2, 120)
        ]

        self.faculty_universities = [
            FacultyUniversity(1, 1),
            FacultyUniversity(2, 1),
            FacultyUniversity(3, 2),
            FacultyUniversity(1, 2)
        ]

    def test_get_university_faculties(self):
        """Тест 1: Список университетов и их факультетов"""
        result = get_university_faculties(self.universities, self.faculties)

        assert len(result) == 2

        assert "Университет А" in result
        assert result["Университет А"] == ["Математический", "Филологический"]

        assert "Университет Б" in result
        assert result["Университет Б"] == ["Экономический"]

        keys = list(result.keys())
        assert keys == ["Университет А", "Университет Б"]

    def test_get_faculty_count(self):
        """Тест 2: Количество факультетов по университетам"""
        result = get_faculty_count(self.universities, self.faculty_universities)

        assert len(result) == 2

        university_names = [name for name, count in result]
        assert "Университет А" in university_names
        assert "Университет Б" in university_names

        for university_name, count in result:
            assert isinstance(university_name, str)
            assert isinstance(count, int)
            assert count == 2

    def test_get_faculties_ending_with_iy(self):
        """Тест 3: Факультеты на 'ий' и их университеты"""
        result = get_faculties_ending_with_iy(
            self.faculties,
            self.universities,
            self.faculty_universities
        )

        assert len(result) == 3

        faculty_names = [name for name, unis in result]
        assert "Филологический" in faculty_names
        assert "Математический" in faculty_names
        assert "Экономический" in faculty_names

        for faculty_name, university_list in result:
            if faculty_name == "Филологический":
                assert len(university_list) == 2
                assert "Университет А" in university_list
                assert "Университет Б" in university_list
                break

if __name__ == "__main__":
    tests = TestUniversityQueries()
    tests.setup_method()

    print("Запуск теста 1...")
    tests.test_get_university_faculties()
    print("✓ Тест 1 пройден")

    print("\nЗапуск теста 2...")
    tests.test_get_faculty_count()
    print("✓ Тест 2 пройден")

    print("\nЗапуск теста 3...")
    tests.test_get_faculties_ending_with_iy()
    print("✓ Тест 3 пройден")

    print("\n✅ Все тесты успешно пройдены!")
