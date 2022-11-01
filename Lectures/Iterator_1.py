class MyIterator():

    def __init__(self, limit, step):
        self.value = 0
        self.limit = limit
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        self.value += self.step
        if self.value >= self.limit:
            raise StopIteration()
        return self.value


my_iter = MyIterator(5, 2)

for v in my_iter:
    print(v)