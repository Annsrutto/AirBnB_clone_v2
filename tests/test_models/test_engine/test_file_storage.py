#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os
from unittest.mock import patch
# from your_module import HBNBCommand  # Adjust the import path as needed

class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

class TestDoCreate(unittest.TestCase):
    """Unit tests for the do_create function of HBNBCommand."""

    def setUp(self):
        """Set up test environment before each test."""
        self.cmd = HBNBCommand()
        HBNBCommand.classes = {'MyClass': MockClass}  # Mock classes dictionary

    def test_class_name_missing(self):
        """Test do_create with missing class name."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.cmd.do_create('')
            self.assertEqual(mock_stdout.getvalue().strip(), "** class name missing **")

    def test_class_does_not_exist(self):
        """Test do_create with non-existent class."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.cmd.do_create('NonExistentClass')
            self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    def test_create_instance_with_no_params(self):
        """Test do_create to create an instance without parameters."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.cmd.do_create('MyClass')
            self.assertIn("MyClass instance created with id", mock_stdout.getvalue())

    def test_create_instance_with_params(self):
        """Test do_create to create an instance with parameters."""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.cmd.do_create('MyClass name="Test Name" number=42')
            output = mock_stdout.getvalue()
            self.assertIn("MyClass instance created with id", output)
            self.assertIn("name set to Test Name", output)
            self.assertIn("number set to 42", output)

class MockClass:
    """Mock class to simulate real class behavior."""
    def __init__(self):
        self.id = "MockID"
        self.attributes = {}

    def save(self):
        """Mock save method."""
        print(f"MyClass instance created with id {self.id}")

    def __setattr__(self, name, value):
        """Override to capture attribute setting."""
        if name != 'id':
            print(f"{name} set to {value}")
        self.attributes[name] = value

if __name__ == '__main__':
    unittest.main()
