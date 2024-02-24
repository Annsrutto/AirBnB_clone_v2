#!/usr/bin/python3
"""This module instantiates storage objects based on the value of
the environment variable HBNB_TYPE_STORAGE"""

import os
from models.engine.file_storage import FileStorage

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
