#!/usr/bin/python3
"""This module contains Test Cases of Console interpreter"""

from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.place import Place
from models import storage
from tests import clear_output


class TestConsole_create(TestCase):
    """Represents test class for create command"""

    def test_file_storage_create(self):
        """Test case for create command by
        using the file storage
        """
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd('create User first_name="Yassine" \
                    last_name="Ait_Mensour" email="yassine1990@alx.com" \
                    age=30')
            user_id = out.getvalue().strip()
            self.assertIn("User.{}".format(user_id), storage.all().keys())
            clear_output(out)
            HBNBCommand().onecmd('show User {}'.format(user_id))
            output = out.getvalue().strip()
            self.assertIn("'first_name': 'Yassine'", output)
            self.assertIn("'last_name': 'Ait Mensour'", output)
            self.assertIn("'email': 'yassine1990@alx.com'", output)
            self.assertIn("'age': 30", output)
            clear_output(out)
            HBNBCommand().onecmd('create Place city_id="0001" user_id="0001" \
                    name="My_little_house" number_rooms=4 number_bathrooms=2 \
                    max_guest=10 price_by_night=300 latitude=37.773972 \
                    longitude=-122.431297')
            place_id = out.getvalue().strip()
            self.assertIn("Place.{}".format(place_id), storage.all().keys())
            clear_output(out)
            HBNBCommand().onecmd('show Place {}'.format(place_id))
            output = out.getvalue().strip()
            self.assertIn("'city_id': '0001'", output)
            self.assertIn("'user_id': '0001'", output)
            self.assertIn("'name': 'My little house'", output)
            self.assertIn("'number_rooms': 4", output)
            self.assertIn("'number_bathrooms': 2", output)
            self.assertIn("'max_guest': 10", output)
            self.assertIn("'price_by_night': 300", output)
            self.assertIn("'latitude': 37.773972", output)
            self.assertIn("'longitude': -122.431297", output)
            clear_output(out)
            HBNBCommand().onecmd('create City name="Sale"')
            city_id = out.getvalue().strip()
            self.assertIn("City.{}".format(city_id), storage.all().keys())
