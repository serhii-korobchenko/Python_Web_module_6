class Kls:
    def __new__(cls, *args):
        print(f"Kls method __new__ called with {args}") #Kls method __new__ called with ('arun',)(1)
        return super().__new__(cls)

    def __init__(self, data):  #data contains *args!!!
        self.data = data

    def printd(self):
        print(self.data)


ik = Kls('arun')  
ik.printd()  # arun (2)