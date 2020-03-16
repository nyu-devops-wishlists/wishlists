"""
Wishlist API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db
from service.service import app, init_db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ Wishlist Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ Runs once before test suite """
        pass

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ Runs once after each test case """
        db.session.remove()
        db.drop_all()

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    
    def test_create_wishlist(self):
        """ Create a new wishlist """
        test_wishlist, resp = self._create_a_wishlist()
        
        
        # Check the data is correct
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist["name"], "Names do not match")
        self.assertEqual(new_wishlist["email"], test_wishlist["email"], "email do not match")
        self.assertEqual(new_wishlist["shared_with1"], test_wishlist["shared_with1"], "shared_with1 do not match")
        self.assertEqual(new_wishlist["shared_with2"], test_wishlist["shared_with2"], "shared_with2 do not match")
        self.assertEqual(new_wishlist["shared_with3"], test_wishlist["shared_with3"], "shared_with3 do not match")

        
        # # Check that the location header was correct
        # resp = self.app.get(location, content_type="application/json")
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_wishlist = resp.get_json()
        # new_wishlist = resp.get_json()
        # self.assertEqual(new_wishlist["name"], test_wishlist["name"], "Names do not match")
        # self.assertEqual(new_wishlist["email"], test_wishlist["email"], "email do not match")
        # self.assertEqual(new_wishlist["shared_with1"], test_wishlist["shared_with1"], "shared_with1 do not match")
        # self.assertEqual(new_wishlist["shared_with2"], test_wishlist["shared_with2"], "shared_with2 do not match")
        # self.assertEqual(new_wishlist["shared_with3"], test_wishlist["shared_with3"], "shared_with3 do not match")

    def test_get_wishlist(self):
        """ Get a single Wishlist """
        # get the id of a wishlist
        test_wishlist, resp = self._create_a_wishlist()
        resp = self.app.get(
            "/wishlists/{}".format(test_wishlist["id"]), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_wishlist["name"])


    def _create_a_wishlist(self):
        """ Factory that creates a wishlist on the server """
        test_wishlist = {
            "name": "Rudi's wishlist",
            "email": "rudi@stern.nyu.edu",
            "shared_with1": "Rebecca Dailey",
            "shared_with2": "Thomas Chao",
            "shared_with3": "Isaias Martin"
        }
        resp = self.app.post(
            "/wishlists",
            json=test_wishlist,
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_wishlist = resp.get_json()
        logging.debug(new_wishlist)
        test_wishlist["id"] = new_wishlist["id"]
        return test_wishlist, resp
