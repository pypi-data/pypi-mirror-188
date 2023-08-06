from abc import ABC, abstractstaticmethod, abstractproperty, abstractmethod, abstractclassmethod
import os

__all__ = ['TableMixin', 'AbstractBaseTable']

class AbstractBaseTable(ABC):

    TABLE_NAME = ''
    NAMESPACE = os.getenv('ECMS_HOST')
    FORIEGN_KEYS = {}

    def __init__(self):
        self.TABLE = self.__class__
        self.TABLE_NAME = self.TABLE_NAME or self.__class__.__name__

    @abstractproperty
    def namespace(self):
        return self.NAMESPACE

    @abstractproperty
    def table(self):
        return self.TABLE.__class__.__name__

    @abstractproperty
    def id(self):
        return f'{self.TABLE_NAME}ID'

    @abstractproperty
    def cols(self):
        return [{k: v} for k, v in self.TABLE.__dict__.items() if '__' not in k]

    @abstractproperty
    def column_names(self):
        return [col for cols in self.cols for col, _ in cols.items()]

    @abstractmethod
    def defaults(self):
        pass

    @abstractmethod
    def foreign_keys(self):
        return self.FORIEGN_KEYS

class TableMixin:
    """
    Table Mixin class to get quick properties from the table
    """
    TABLE_NAME = ''
    NAMESPACE = os.getenv('ECMS_HOST')
    FORIEGN_KEYS = {}

    def __init__(self):
        self.TABLE = self.__class__
        self.TABLE_NAME = self.__class__.__name__

    @property
    def namespace(self):
        return self.NAMESPACE

    @property
    def table(self):
        return self.TABLE.__class__.__name__

    @property
    def id(self):
        return f'{self.TABLE_NAME}ID'

    @property
    def cols(self):
        return [{k: v} for k, v in self.TABLE.__dict__.items() if '__' not in k]

    @property
    def column_names(self):
        return [col for cols in self.cols for col, _ in cols.items()]


class DbTypes:
    
    @staticmethod
    def INT(length=2, friendly=''):
        return {
            'type': 'INT', 
            'length': length, 
            'friendly_name': friendly
        }

    @staticmethod
    def CHAR(length=30, friendly=''):
        return {
            'type': 'CHAR', 
            'length': length, 
            'friendly_name': friendly
        }

    @staticmethod
    def DATE(length=9, friendly=''):
        return {
            'type': 'DATE', 
            'length': length, 
            'friendly_name': friendly
        }

    @staticmethod
    def TIMESTAMP(length=9, friendly=''):
        return {
            'type': 'TIMESTAMP', 
            'length': length, 
            'friendly_name': friendly
        }