#!/usr/bin/python3
"""Defines unittests for models/place.py
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(pl))
        self.assertNotIn("city_id", pl.__dict__)

    def test_user_id_is_public_class_attribute(self):
        plaa = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(plaa))
        self.assertNotIn("user_id", plaa.__dict__)

    def test_name_is_public_class_attribute(self):
        plaa = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(plaa))
        self.assertNotIn("name", plaa.__dict__)

    def test_description_is_public_class_attribute(self):
        plaa = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(plaa))
        self.assertNotIn("desctiption", plaa.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(pl))
        self.assertNotIn("number_rooms", pl.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(pl))
        self.assertNotIn("number_bathrooms", pl.__dict__)

    def test_latitude_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(pl))
        self.assertNotIn("latitude", pl.__dict__)

    def test_longitude_is_public_class_attribute(self):
        pl = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(pl))
        self.assertNotIn("longitude", pl.__dict__)

    def test_two_places_unique_ids(self):
        pl1aa = Place()
        pl2aa = Place()
        self.assertNotEqual(pl1aa.id, pl2aa.id)

    def test_two_places_different_created_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.created_at, pl2.created_at)

    def test_two_places_different_updated_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.updated_at, pl2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        pl = Place()
        pl.id = "123456"
        pl.created_at = pl.updated_at = dt
        plstr = pl.__str__()
        self.assertIn("[Place] (123456)", plstr)
        self.assertIn("'id': '123456'", plstr)
        self.assertIn("'created_at': " + dt_repr, plstr)
        self.assertIn("'updated_at': " + dt_repr, plstr)

    def test_args_unused(self):
        pl = Place(None)
        self.assertNotIn(None, pl.__dict__.values())

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests save method of the Place class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        plaa = Place()
        sleep(0.05)
        first_updated_at = plaa.updated_at
        plaa.save()
        self.assertLess(first_updated_at, plaa.updated_at)

    def test_two_saves(self):
        plaa = Place()
        sleep(0.05)
        first_updated_at = plaa.updated_at
        plaa.save()
        second_updated_at = plaa.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        plaa.save()
        self.assertLess(second_updated_at, plaa.updated_at)

    def test_save_with_arg(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.save(None)

    def test_save_updates_file(self):
        plaa = Place()
        plaa.save()
        plid = "Place." + plaa.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        pl = Place()
        self.assertIn("id", pl.to_dict())
        self.assertIn("created_at", pl.to_dict())
        self.assertIn("updated_at", pl.to_dict())
        self.assertIn("__class__", pl.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        pl = Place()
        pl_dict = pl.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        pl = Place()
        pl.id = "123456"
        pl.created_at = pl.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(pl.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        plaa = Place()
        self.assertNotEqual(plaa.to_dict(), plaa.__dict__)

    def test_to_dict_with_arg(self):
        plaa = Place()
        with self.assertRaises(TypeError):
            plaa.to_dict(None)


if __name__ == "__main__":
    unittest.main()

