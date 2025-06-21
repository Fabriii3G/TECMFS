class HashEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashMap:
    def __init__(self, size=20000):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        h = 0
        for char in key:
            h = (h * 31 + ord(char)) % self.size
        return h

    def put(self, key, value):
        index = self._hash(key)
        original = index
        while self.table[index] is not None and self.table[index].key != key:
            index = (index + 1) % self.size
            if index == original:
                raise Exception("HashMap is full")
        self.table[index] = HashEntry(key, value)

    def get(self, key):
        index = self._hash(key)
        original = index
        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.size
            if index == original:
                break
        return None
