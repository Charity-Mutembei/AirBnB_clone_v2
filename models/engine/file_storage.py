#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored with key clsname.objectID
    """
    __file_path = "file.json"
    __objects = {}
    __clsdict = {
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self, cls=None):
        '''
        Return the dictionary
        '''
        if cls is None:
            return self.__objects
        else:
            dict = {}
            for k, v in self.__objects.items():
                name = k.split('.')
                if name[0] in str(cls):
                    dict[k] = v
            return dict
    
    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON file path
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete an object from __objects if the given object exists
        Args:
            obj: given object
        Exceptions:
            KeyError: when object doesn't exist
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(key, None)
            # try:
            #     del self.__objects[key]
            # except KeyError:
            #     pass

    def close(self):
        """deserializing the JSON file to objects
        """
        self.reload()
