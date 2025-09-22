# class User:
#     test_number = 10
#     def __init__(self, name, age, breed): #если __init__ несколько, вызовется последний
#         # print("Hello! It's me")
#         self.name = name
#         self.age = age
#         self.breed = breed
#
#     def add(self):
#         print(f"Let's add one cat {self.name}, {self.age}, {self.breed}")
#
#     def __str__(self):
#         return f"{self.name}, {self.age}, {self.breed}, you're the best!"
#
# test_number = 5 # несмотря на инициализацию поля test_number в User, изменения вне класса тоже отразятся внутри него
# cat = User("May", 13, "Ragdoll")
# cat.test_number = 15
# print(cat.age, test_number, cat.test_number)
# print(cat.__dict__)
#
# added_cat = User("Mine", 9, "British shorthair")
# added_cat.add()
# print(str(added_cat))

"""
cat = User()
cat.name = 'May' # .name - атрибуты
cat.age = 13
cat.breed = "Ragdoll"

print(cat.name, cat.age, cat.breed)
"""

class Matrix:
    def __init__(self, data):
        if not data or not all(isinstance(row, list) for row in data):
            raise ValueError("Matrix must be a non-empty list of lists")
        row_length = len(data[0])
        for row in data:
            if len(row) != row_length:
                raise ValueError("All rows must have the same number of columns")
        self.data = data
        self.rows = len(data)
        self.cols = row_length

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")
        result = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction")
        result = [[self.data[i][j] - other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Number of columns of the first matrix must be equal to number of rows of the second matrix")
        result = [[sum(self.data[i][k] * other.data[k][j]
                       for k in range(self.cols))
                   for j in range(other.cols)] for i in range(self.rows)]
        return Matrix(result)

