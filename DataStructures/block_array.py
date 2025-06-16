class BlockArray:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [None] * capacity
        self.size = 0

    def add(self, value):
        if self.size < self.capacity:
            self.data[self.size] = value
            self.size += 1

    def get(self, index):
        if 0 <= index < self.size:
            return self.data[index]
        else:
            raise IndexError("Index out of bounds")

    def length(self):
        return self.size
