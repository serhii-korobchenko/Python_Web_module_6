class MyMeta(type):
    def __new__(*args):
        print(f'MyMeta __new__ called with {args}') #MyMeta __new__ called with (<class '__main__.MyMeta'>, 'A', (), {'__module__': '__main__', '__qualname__': 'A', '__init__': <function A.__init__ at 0x000001AE7F2E2F80>})
        return type.__new__(*args)

    def __init__(*args):
        print(f'MyMeta __init__ called with {args}') #MyMeta __init__ called with (<class '__main__.A'>, 'A', (), {'__module__': '__main__', '__qualname__': 'A', '__init__': <function A.__init__ at 0x000001AE7F2E2F80>})


class A(metaclass=MyMeta):
    def __init__(self, data):
        
        self.data = data