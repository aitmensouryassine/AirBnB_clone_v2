#!/usr/bin/python3
"""This module contains test case for db_storage"""
from unittest import TestCase, skipIf
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime
import os
from models import storage_type


@skipIf(storage_type != 'db',
        "db_storage test not supported")
class TestDBStorage(TestCase):
    """DBStorage test class"""
    def new_and_save_db_storage(self):
        """testing  the new and save methods"""
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        u_dict = {'first_name': 'Yassine',
                  'last_name': 'Ait Mensour',
                  'email': 'yassine@test.com',
                  'password': 'azerty123'}
        new_user = User(**u_dict)
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
        db.close()

    def test_new_db_storage(self):
        """ Tests if a new object is added to the database """
        u_new = User(
            email='hajar2023@gmail.com',
            password='password1991',
            first_name='Shashou',
            last_name='Chamss'
        )
        self.assertFalse(u_new in storage.all().values())
        u_new.save()
        self.assertTrue(u_new in storage.all().values())
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(u_new.id))
        result = cursor.fetchone()
        self.assertFalse(result is None)
        self.assertIn('hajar2023@gmail.com', result)
        self.assertIn('password1991', result)
        self.assertIn('Shashou', result)
        self.assertIn('Chamss', result)
        cursor.close()
        dbc.close()

    def test_delete_db_storage(self):
        """ Tests if an object is deleted from the database """
        new = User(
            email='hajar2023@gmail.com',
            password='password1991',
            first_name='Shashou',
            last_name='Chamss'
        )
        u_key = 'User.{}'.format(new.id)
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
        self.assertIn('hajar2023@gmail.com', result)
        self.assertIn('password1991', result)
        self.assertIn('Shashou', result)
        self.assertIn('Chamss', result)
        self.assertIn(u_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(u_key, storage.all(User).keys())
        cursor.close()
        dbc.close()

    def test_reload_db_storage(self):
        """ Tests the reloading of the database session """
        db_reload = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db_reload.cursor()
        cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                'XXXX-XXXX-XXXX-XXXX-XXXX',
                str(datetime.now()),
                str(datetime.now()),
                'yass_haj@alx.com',
                'pass@258',
                'Noura',
                'Fassi',
            ]
        )
        u_id = 'XXXX-XXXX-XXXX-XXXX-XXXX'
        self.assertNotIn('User.{}'.format(u_id), storage.all())
        db_reload.commit()
        storage.reload()
        self.assertIn('User.{}'.format(u_id), storage.all())
        cursor.close()
        db_reload.close()

    def test_save_db_storage(self):
        """tests object is successfully saved to database """
        new = User(
            email='hajar2023@gmail.com',
            password='password1991',
            first_name='Shashou',
            last_name='Chamss'
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
