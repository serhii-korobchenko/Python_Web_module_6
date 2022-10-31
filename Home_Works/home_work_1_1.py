""" Напишите классы сериализации контейнеров с данными Python в json, bin файлы. 
Сами классы должны соответствовать общему интерфейсу (абстрактному базовому классу) 
SerializationInterface. """

from abc import abstractmethod, ABC
import pickle
import json

class SerializationInterface(ABC):
    
    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def logging(self):
        pass

class SerializationBin(SerializationInterface):
    
    def serialize(self):
        file_name = 'data.bin'
        with open(file_name, "wb") as fh:
            pickle.dump(some_data, fh)


    def logging(self):
        
        file_name = "report.txt"
        with open(file_name, "a") as rpt:          
            rpt.write("Information serialized in bin format\n")


class SerializationJson(SerializationInterface):
    
    def serialize(self):
        file_name = 'data.json'
        with open(file_name, "w") as fh:
            json.dump(some_data, fh)


    def logging(self):       
        file_name = "report.txt"
        with open(file_name, "a") as rpt:          
            rpt.write("Information serialized in json format\n")

if __name__ == '__main__':
        
    some_data = {}

    bin_1 = SerializationBin()
    json_1 = SerializationJson()

    bin_1.serialize()
    bin_1.logging()
    json_1.serialize()
    json_1.logging()

