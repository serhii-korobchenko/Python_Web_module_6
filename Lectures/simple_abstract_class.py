class MyABC:
    def foo(self):
        raise NotImplementedError()

    def bar(self):
        raise NotImplementedError()


class ActualMy(MyABC):
    def foo(self):
        print('foo')


a = ActualMy()
a.foo()     # foo
a.bar()     # raises NotImplementedError