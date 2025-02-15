class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {"length": self.length}
        yield {"width": self.width}


rect = Rectangle(10, 5)

# Iterating over the Rectangle instance
for attribute in rect:
    print(attribute)
