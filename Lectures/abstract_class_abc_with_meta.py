from abc import abstractmethod, ABCMeta


class MyBaseClass(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def baz(self):
        pass


class Child(MyBaseClass):
    pass


c = Child()  # TypeError: Can't instantiate abstract class Child with abstract methods baz, foo