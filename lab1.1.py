import math

class BiquadraticEquation:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.d = b**2 - 4*a*c
        self.roots = []

    def solve(self):
        print(f"\nРешаем уравнение: {self.a}x^4 + {self.b}x^2 + {self.c} = 0")
        print(f"Дискриминант D = {self.d}")

        if self.d < 0:
            print("Дискриминант отрицательный. Корней нет.")
            return

        y1 = (-self.b + math.sqrt(self.d)) / (2 * self.a)
        y2 = (-self.b - math.sqrt(self.d)) / (2 * self.a)

        print(f"y1 = {y1}, y2 = {y2}")

        if y1 >= 0:
            x1 = math.sqrt(y1)
            x2 = -math.sqrt(y1)
            self.roots.append(x1)
            self.roots.append(x2)
            print(f"Из y1 получили: x1 = {x1}, x2 = {x2}")

        if y2 >= 0 and y2 != y1:
            x3 = math.sqrt(y2)
            x4 = -math.sqrt(y2)
            self.roots.append(x3)
            self.roots.append(x4)
            print(f"Из y2 получили: x3 = {x3}, x4 = {x4}")

        if y1 == 0 or y2 == 0:
            if 0 not in self.roots:
                self.roots.append(0)
                print("Получили корень: x = 0")

    def show_roots(self):
        if not self.roots:
            print("Действительных корней нет.")
        else:
            unique_roots = []
            for root in self.roots:
                if root not in unique_roots:
                    unique_roots.append(root)
            unique_roots.sort()

            print(f"\nНайдено {len(unique_roots)} корней:")
            for i, root in enumerate(unique_roots, 1):
                print(f"x{i} = {root}")


def get_coefficient(name):
    while True:
        try:
            value = float(input(f"Введите коэффициент {name}: "))

            if name == "A" and value == 0:
                print("Коэффициент A не может быть равен 0!")
                continue

            return value
        except ValueError:
            print("Ошибка! Введите число.")


def main():
    print("РЕШЕНИЕ БИКВАДРАТНОГО УРАВНЕНИЯ")
    print("Уравнение: Ax^4 + Bx^2 + C = 0")

    while True:
        print("\nВведите коэффициенты")
        a = get_coefficient("A")
        b = get_coefficient("B")
        c = get_coefficient("C")

        equation = BiquadraticEquation(a, b, c)

        equation.solve()
        equation.show_roots()

        choice = input("Решить еще одно уравнение? (да/нет): ").lower()
        if choice not in ['да', 'д', 'yes', 'y']:
            print("До свидания!")
            break

if __name__ == "__main__":
    main()
