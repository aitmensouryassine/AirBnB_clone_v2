#!/usr/bin/python3
""" Module for testing database storage"""
from unittest import TestCase, skipIf
from models import storage
import os
import MySQLdb
from models.user import User
from models import storage_type


@skipIf(storage_type != 'db',
        'db_storage test not supported')
class TestDBStorage(TestCase):
    """Represents Test class for DB storage"""
    def test_new_db_storage(self):
        """Tests the new method"""
        db = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                             port=3306,
                             user=os.getenv("HBNB_MYSQL_USER"),
                             passwd=os.getenv("HBNB_MYSQL_PWD"),
                             db=os.getenv("HBNB_MYSQL_DB"))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        count = cur.fetchone()
        cur.close()
        db.close()
        user_dict = {'first_name': 'HAJAR',
                     'last_name': 'ALX',
                     'email': 'hajar@alx.com',
                     'password': 'Yassine1991*$'}
        user = User(**user_dict)
        user.save()
        db = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                             port=3306,
                             user=os.getenv("HBNB_MYSQL_USER"),
                             passwd=os.getenv("HBNB_MYSQL_PWD"),
                             db=os.getenv("HBNB_MYSQL_DB"))
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        new_count = cur.fetchone()
        cur.close()
        db.close()
        self.assertEqual(new_count[0], count[0] + 1)
