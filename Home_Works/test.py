class MetaCounter(type):
    
    _counter = {}

    def __new__(cls, name, bases, dict):
        cls._counter[name] = 0
        return super().__new__(cls, name, bases, dict)

    def __call__(cls, *args, **kwargs):
        cls._counter[cls.__name__] += 1
        print(f'Instantiated {cls._counter[cls.__name__]} objects of class {cls}!')
        return super().__call__(*args, **kwargs)

class Foo(metaclass=MetaCounter):
    pass
class Bar(metaclass=MetaCounter):
    pass


x = Foo()
y = Foo()
z = Foo()
a = Bar()
b = Bar()
print(MetaCounter._counter)
# {'Foo': 3, 'Bar': 2} --> OK!
print(Foo._counter)
# {'Foo': 3, 'Bar': 2} --> I'd like it printed just "3"
print(Bar._counter) 
# {'Foo': 3, 'Bar': 2} --> I'd like it printed just "2"