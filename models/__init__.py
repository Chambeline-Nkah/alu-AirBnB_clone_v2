#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
# from models.user import User
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import os
from dotenv import find_dotenv, load_dotenv


env_path = find_dotenv()
load_dotenv(env_path)

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    # from models.engine.db_storage import DBStorage

    storage = DBStorage()
    storage.reload()
else:
    # from models.engine.file_storage import FileStorage

    storage = FileStorage()
    storage.reload()
