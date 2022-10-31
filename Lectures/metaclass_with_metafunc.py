def meta_func(name, bases, attrs):
    print('meta function called with', name, bases, attrs) # meta function called with Kls () {'__module__': '__main__', '__qualname__': 'Kls', 'some': 2, 'print_some': <function Kls.print_some at 0x000001CEE4282EF0>}
    attrs["always_add"] = 42
    return type(name, bases, attrs)


class Kls(metaclass=meta_func):
    some = 2

    def print_some(self):
        print(self.some)

print(Kls.always_add)   # 42