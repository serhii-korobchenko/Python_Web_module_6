def class_decorator(cls):
    class Inner(cls):
        def print_hello(self):
            print("hello")
    return Inner

@class_decorator
class A:
    pass

a = A()
a.print_hello()     # hello
print(a)            # <__main__.class_decorator.<locals>.Inner object at 0x7f8477ac5d30>