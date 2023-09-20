#!/usr/bin/python3
"""This module contains test cases for db_storage"""
from unittest import TestCase, skipIf
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime
import os
from models import storage_type
from models.engine.db_storage import DBStorage


@skipIf(storage_type != 'db',
        'db_storage is not supported')
class TestDBStorage(TestCase):
    """db storage Class"""

    def test_db_storage_doc(self):
        """test case for docstring of DBStorage Class"""
        self.assertIsNot(DBStorage.__doc__, None)

    '''def new_and_save_db_storage(self):
        """test case for new and save methods"""
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'yassine',
                           'last_name': 'ALX',
                           'email': 'yassine@alx.com',
                           'password': 'pass123*$'})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        old_count = cur.fetchone()
        cur.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        new_count = cur.fetchone()
        self.assertEqual(new_count[0], old_count[0] + 1)
        cur.close()
        db.close()'''

    def test_new_db_storage(self):
        """test case if New object is added to database"""
        new = User(
            email='hajar2023@alx.com',
            password='password@123',
            first_name='Chamss',
            last_name='Shashou'
        )
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('hajar2023@alx.com', result)
        self.assertIn('password@123', result)
        self.assertIn('Chamss', result)
        self.assertIn('Shashou', result)
        cursor.close()
        dbc.close()

    def test_delete_db_storage(self):
        """test case if object is deleted from database"""
        new = User(
            email='hajar2023@alx.com',
            password='password@123',
            first_name='Chamss',
            last_name='Shashou'
        )
        obj_key = 'User.{}'.format(new.id)
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        new.save()
        self.assertTrue(new in storage.all().values())
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('hajar2023@alx.com', result)
        self.assertIn('password@123', result)
        self.assertIn('Chamss', result)
        self.assertIn('Shashou', result)
        self.assertIn(obj_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())
        cursor.close()
        dbc.close()

    '''def test_reload_db_storage(self):
        """Test case for reload method"""
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                'xxxx-xxxx-xxxx-xxxx',
                str(datetime.now()),
                str(datetime.now()),
                'hajarTest@alx.com',
                'hello123',
                'Yassine',
                'Ait',
            ]
        )
        self.assertNotIn('User.xxxx-xxxx-xxxx-xxxx', storage.all())
        dbc.commit()
        storage.reload()
        self.assertIn('User.xxxx-xxxx-xxxx-xxxx', storage.all())
        cursor.close()
        dbc.close()'''

    def test_save_db_storage(self):
        """ test case if object is saved to database"""
        new = User(
            email='hajar2023@alx.com',
            password='password@123',
            first_name='Chamss',
            last_name='Shashou'
        )
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        old_cnt = cursor.fetchone()[0]
        self.assertTrue(result is None)
        self.assertFalse(new in storage.all().values())
        new.save()
        dbc1 = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor1 = dbc1.cursor()
        cursor1.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor1.fetchone()
        cursor1.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cursor1.fetchone()[0]
        self.assertFalse(result is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new in storage.all().values())
        cursor1.close()
        dbc1.close()
        cursor.close()
        dbc.close()
