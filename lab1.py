import math
import sys

def get_coefficient(index, name):
    """Функция для получения коэффициента из аргументов командной строки или ввода с клавиатуры"""
    if len(sys.argv) > index + 1:
        try:
            value = float(sys.argv[index + 1])
            print(f"Коэффициент {name} = {value} (из командной строки)")
            return value
        except ValueError:
            print(f"Некорректное значение коэффициента {name} в командной строке. Требуется ввод с клавиатуры.")

    while True:
        try:
            value = float(input(f"Введите коэффициент {name}: "))
            return value
        except ValueError:
            print("Ошибка! Введите действительное число.")

def solve_biquadratic(a, b, c):
    """Функция для решения биквадратного уравнения"""
    print(f"\nУравнение: {a}x^4 + {b}x^2 + {c} = 0")

    D = b**2 - 4*a*c
    print(f"Дискриминант D = {D}")

    roots = []

    if D < 0:
        print("Дискриминант отрицательный.")
    else:
        y1 = (-b + math.sqrt(D)) / (2 * a)
        y2 = (-b - math.sqrt(D)) / (2 * a)

        print(f"y1 = {y1}, y2 = {y2}")

        if y1 >= 0:
            x1 = math.sqrt(y1)
            x2 = -x1
            roots.extend([x1, x2])
            print(f"Из y1 = {y1} получены корни: x1 = {x1}, x2 = {x2}")

        if y2 >= 0 and y2 != y1:
            x3 = math.sqrt(y2)
            x4 = -math.sqrt(y2)
            roots.extend([x3, x4])
            print(f"Из y2 = {y2} получены корни: x3 = {x3}, x4 = {x4}")

        if not roots:
            print("Нет действительных корней (y1 и y2 отрицательные).")

    return roots

def main():
    print("Решение биквадратного уравнения вида: Ax^4 + Bx^2 + C = 0")
    print("=" * 50)

    a = get_coefficient(0, 'A')
    b = get_coefficient(1, 'B')
    c = get_coefficient(2, 'C')

    while a == 0:
        print("Ошибка! Коэффициент A не может быть равен 0 для биквадратного уравнения.")
        a = get_coefficient(0, 'A')

    roots = solve_biquadratic(a, b, c)

    if roots:
        roots.sort()
        print(f"\nДействительные корни уравнения: {roots}")
        print("Корни в отсортированном порядке:")
        for i, root in enumerate(roots, 1):
            print(f"x{i} = {root:.6f}")
    else:
        print("\nДействительных корней нет.")

if __name__ == "__main__":
    main()
