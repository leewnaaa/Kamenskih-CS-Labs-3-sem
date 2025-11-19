import math

def get_number_input(prompt):
    while True:
        try:
            number = float(input(prompt))
            return number
        except ValueError:
            print("Ошибка! Пожалуйста, введите число.")

def solve_biquadratic():
    print("")
    print("Решение биквадратного уравнения")
    print("Уравнение имеет вид: Ax⁴ + Bx² + C = 0")

    print("\nВведите коэффициенты уравнения:")
    while True:
        a = get_number_input("Введите коэффициент A: ")
        if a != 0:
            break
        print("Ошибка! Коэффициент A не может быть равен 0.")

    b = get_number_input("Введите коэффициент B: ")
    c = get_number_input("Введите коэффициент C: ")

    print(f"\nВаше уравнение: {a}x^4 + {b}x^2 + {c} = 0")

    discriminant = b * b - 4 * a * c
    print(f"Дискриминант D = {discriminant}")

    if discriminant < 0:
        print("Дискриминант отрицательный. Действительных корней нет.")
        return

    y1 = (-b + math.sqrt(discriminant)) / (2 * a)
    y2 = (-b - math.sqrt(discriminant)) / (2 * a)

    print(f"\nНайдены промежуточные значения:")
    print(f"y1 = {y1} (где y = x^2)")
    print(f"y2 = {y2} (где y = x^2)")

    roots = []

    if y1 > 0:
        root1 = math.sqrt(y1)
        root2 = -root1
        roots.append(root1)
        roots.append(root2)
        print(f"Из y1 = {y1} > 0 получаем корни: x1 = {root1}, x2 = {root2}")
    elif y1 == 0:
        roots.append(0)
        print(f"Из y1 = 0 получаем корень: x = 0")

    if y2 > 0 and y2 != y1:
        root3 = math.sqrt(y2)
        root4 = -root3
        roots.append(root3)
        roots.append(root4)
        print(f"Из y2 = {y2} > 0 получаем корни: x3 = {root3}, x4 = {root4}")
    elif y2 == 0 and y1 != 0:
        roots.append(0)
        print(f"Из y2 = 0 получаем корень: x = 0")

    print("\nРЕЗУЛЬТАТЫ:")

    if len(roots) == 0:
        print("Действительных корней нет.")
    else:
        roots.sort()
        print(f"Найдено действительных корней: {len(roots)}")

        for i, root in enumerate(roots, 1):
            if root.is_integer():
                print(f"x{i} = {int(root)}")
            else:
                print(f"x{i} = {root:.6f}")

while True:
    solve_biquadratic()

    again = input("\nХотите решить еще одно уравнение? (да/нет): ").lower()
    if again not in ['да', 'д', 'yes', 'y']:
        break
    print()
