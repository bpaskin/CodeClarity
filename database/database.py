from abc import ABC, abstractmethod
class Database(ABC):

    @abstractmethod
    def logon(self, url, username, password, certificate):
        pass
          
    @abstractmethod
    def write_record(self, index, data):
        pass

    @abstractmethod
    def read_record(self, index, data):
        pass

    @abstractmethod
    def search_records(self, index, search):
        pass

    @abstractmethod
    def delete_record(self, index, id):
        pass


    @abstractmethod
    def create_table(self, index):
        pass
