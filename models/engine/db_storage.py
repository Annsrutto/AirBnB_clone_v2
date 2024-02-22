#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}', pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a class. If cls=None, query all objects."""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        cls_dict = {
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
        }

        obj_dict = {}
        if cls is None:
            for cls_name in cls_dict:
                objs = self.__session.query(cls_dict[cls_name]).all()
                for obj in objs:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    obj_dict[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f'{cls.__name__}.{obj.id}'
                obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload the database session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
