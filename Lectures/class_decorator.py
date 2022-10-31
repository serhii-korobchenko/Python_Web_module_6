class Decorator:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def __call__(self, func):
        def inner(*args, **kwargs):
            for arg in args:
                if arg < self.min_val or arg > self.max_val:
                    raise ValueError('Out of range')
            return func(*args)
        return inner


@Decorator(0, 5)
def foo(x, y):
    pass


@Decorator(-5, 0)
def baz(x, y):
    pass


foo(1, 4)