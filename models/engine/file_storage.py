#!/usr/bin/python3
"""contains a class FileStorage that serializes instances
to a JSON file and deserializes JSON file to instances"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format."""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns the list of objects of one type of class.
        If cls is None, returns all objects.
        """
        if cls is None:
            return self.__objects
        else:
            cls_name = cls.__name__ if isinstance(cls, type) else cls
            return {k: v for k, v in self.__objects.items()
                    if k.split('.')[0] == cls_name}

    def new(self, obj):
        """Adds new object to storage dictionary."""
        key = obj.__class__.__name__ + '.' + obj.id
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file."""
        temp = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(temp, f)

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        If obj is equal to None, the method does not do anything.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def reload(self):
        """Loads storage dictionary from file."""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
            for key, val in temp.items():
                cls_name = key.split('.')[0]
                if cls_name in classes:
                    self.__objects[key] = classes[cls_name](**val)
        except FileNotFoundError:
            pass
