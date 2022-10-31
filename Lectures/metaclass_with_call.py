class MyMeta(type):

    def __call__(cls, *args):
        print('MyMeta __call__ called') #MyMeta __call__ called(1)
        print('class:', cls)            #class: <class '__main__.Kls'>(2)
        print('args:', args)            #args: ('arun',)(3)
        instance =  object.__new__(cls)
        instance.__init__(*args)
        return instance


class Kls(metaclass=MyMeta):

    def __init__(self, data):
        print("I am Kls method __init__") #I am Kls method __init__ (4)
        self.data = data

    def printd(self):
        print(self.data)


ik = Kls('arun')