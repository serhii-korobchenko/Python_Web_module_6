from abc import abstractmethod, ABC


class MyBaseClass(ABC):
    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def baz(self):
        pass


class Child(MyBaseClass):
    pass


c = Child() 