# Пример 1: Вывод текста
print("Hello, World!")

# Пример 2: Типы данных
x = 10      # int
y = 3.14    # float
z = 2 + 3j  # complex
print(type(y))

# Пример 3: Работа со строками
text = "Python - лучший язык!"
print(text[0])

# Пример 4: Списки
numbers = [1, 2, 3, 4, 5]
print(numbers[2])

# Пример 5: Кортежи
point = (10, 20)
print(point[1])

# Пример 6: Словари
person = {"name": "Alice", "age": 25}
print(person["name"])

# Пример 7: Множества
unique_numbers = {1, 2, 3, 3, 2, 1}
print(unique_numbers)

# Пример 8: Условные операторы
age = 18
if age >= 18:
    print("Доступ разрешен")
else:
    print("Доступ запрещен")

# Пример 9: Цикл for
for i in range(5):
    print(i)

# Пример 10: Цикл while
x = 0
while x < 5:
    print(x)
    x += 1

# Пример 11: Функции
def greet(name):
    return f"Привет, {name}!"
print(greet("Анна"))

# Пример 12: Функция с параметром по умолчанию
def power(x, n=2):
    return x ** n
print(power(3))  # 9
print(power(3, 3))  # 27
