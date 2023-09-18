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
        user_dict = {'first_name': 'MANAL',
                     'last_name': 'ALX',
                     'email': 'manal@alx.com',
                     'password': 'Yassine1991*$'}
        user = User(**user_dict)
        print("new:", user.id)
        user.save()
        cur.execute("SELECT COUNT(*) FROM users")
        new_count = cur.fetchone()
        cur.close()
        db.close()
        # self.assertEqual(new_count[0], count[0] + 1)

    def test_save_db_storage(self):
        """Tests save method"""
        user = User(
                email='yassine90@alx.com',
                password='password123',
                first_name='Yassine',
                last_name='ALX'
                )

        db1 = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                              port=3306,
                              user=os.getenv("HBNB_MYSQL_USER"),
                              passwd=os.getenv("HBNB_MYSQL_PWD"),
                              db=os.getenv("HBNB_MYSQL_DB"))
        cur1 = db1.cursor()
        cur1.execute('SELECT * FROM users WHERE id="{}"'.format(user.id))
        result = cur1.fetchone()
        self.assertTrue(result is None)
        self.assertFalse(user in storage.all().values())
        cur1.execute('SELECT COUNT(*) FROM users')
        old_count = cur1.fetchone()[0]
        cur1.close()
        db1.close()
        user.save()
        db2 = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                              port=3306,
                              user=os.getenv("HBNB_MYSQL_USER"),
                              passwd=os.getenv("HBNB_MYSQL_PWD"),
                              db=os.getenv("HBNB_MYSQL_DB"))
        cur2 = db2.cursor()
        cur2.execute('SELECT * FROM users WHERE id="{}"'.format(user.id))
        result = cur2.fetchone()
        self.assertFalse(result is None)
        self.assertTrue(user in storage.all().values())
        cur2.execute('SELECT COUNT(*) FROM users')
        self.assertEqual(old_count + 1, cur2.fetchone()[0])
        cur2.close()
        db2.close()

    def test_delete_db_storage(self):
        """tests delete method"""
        new = User(
                email='hajar@alx.com',
                password='password123',
                first_name='Hajar',
                last_name='ALX')
        new.save()
        print("delete:", new.id)
        self.assertTrue(new in storage.all().values())
        del_db = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                                 port=3306,
                                 user=os.getenv("HBNB_MYSQL_USER"),
                                 passwd=os.getenv("HBNB_MYSQL_PWD"),
                                 db=os.getenv("HBNB_MYSQL_DB"))
        del_cur = del_db.cursor()
        del_cur.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        usr = del_cur.fetchone()
        self.assertFalse(usr is None)
        self.assertIn('hajar@alx.com', usr)
        self.assertIn('password123', usr)
        self.assertIn('Hajar', usr)
        self.assertIn('ALX', usr)
        u_key = 'User.{}'.format(new.id)
        self.assertIn(u_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(u_key, storage.all(User).keys())
        del_cur.close()
        del_db.close()
