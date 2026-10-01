"""
Занятие 1. Практика: переменные и арифметика.

Вместо ... напиши выражение, которое считает ответ. Числа руками не подставляй:
не piece_price = 56.25, а piece_price = pizza_price / pieces.

Запуск: правый клик по файлу → Run. Внизу появятся OK и FAIL.
"""

# Задача 1. Пицца стоит 450 рублей, в ней 8 кусков. Сколько стоит один кусок?
pizza_price = 450
pieces = 8
piece_price = ...

# Задача 2. 8 кусков делят на 3 друзей поровну, целыми кусками.
# Сколько кусков достанется каждому (each) и сколько останется (left)?
friends = 3
each = ...
left = ...

# Задача 3. Фильм идёт 135 минут. Сколько это целых часов (hours) и минут (minutes)?
film = 135
hours = ...
minutes = ...

# Задача 4. Средняя оценка за три контрольные.
mark1 = 5
mark2 = 4
mark3 = 4
average = ...

# Задача 5. Собери строку через f-строку: "Привет, Аня! Через 5 лет тебе будет 23."
name = "Аня"
age = 18
greeting = ...

# Задача 6. Комната 3.5 на 4 метра. Площадь (area) и стоимость ламината (cost),
# если квадратный метр стоит 1200 рублей.
width = 3.5
length = 4
area = ...
cost = ...


# ---------------- Проверки (не менять) ----------------

def check(what, actual, expected):
    if actual is ...:
        print(f"FAIL  {what}  ещё не сделано")
    elif actual == expected or (isinstance(expected, float) and abs(actual - expected) < 0.01):
        print(f"OK    {what}")
    else:
        print(f"FAIL  {what}  ожидалось {expected!r}, получено {actual!r}")


check("Задача 1: piece_price", piece_price, 56.25)
check("Задача 2: each", each, 2)
check("Задача 2: left", left, 2)
check("Задача 3: hours", hours, 2)
check("Задача 3: minutes", minutes, 15)
check("Задача 4: average", average, 4.33)
check("Задача 5: greeting", greeting, "Привет, Аня! Через 5 лет тебе будет 23.")
check("Задача 6: area", area, 14.0)
check("Задача 6: cost", cost, 16800.0)
