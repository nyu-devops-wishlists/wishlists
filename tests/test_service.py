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
from service.models import Wishlist, Item, db
from service.service import app, init_db
from tests.factories import WishlistFactory

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
#  H E L P E R   M E T H O D S
######################################################################

    def _create_wishlists(self, count):
        """ Factory method to create wishlists in bulk """
        wishlists = []
        for _ in range(count):
            test_wishlist = WishlistFactory()
            resp = self.app.post(
                "/wishlists", json=test_wishlist.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test wishlist"
            )
            new_wishlist = resp.get_json()
            test_wishlist.id = new_wishlist["id"]
            wishlists.append(test_wishlist)
        return wishlists


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

######################################################################
#  W I S H L I S T   T E S T   C A S E S   H E R E 
######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_create_wishlist(self):
        """ Create a new wishlist """
        wishlist = WishlistFactory()
        resp = self.app.post(
            "/wishlists", 
            json=wishlist.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        logging.debug("Location header: %s", location)

        # Check the data is correct
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"], wishlist.name, "Names do not match")
        self.assertEqual(new_wishlist["email"], wishlist.email, "email do not match")
        self.assertEqual(new_wishlist["shared_with1"], wishlist.shared_with1, "shared_with1 do not match")
        self.assertEqual(new_wishlist["shared_with2"], wishlist.shared_with2, "shared_with2 do not match")
        self.assertEqual(new_wishlist["shared_with3"], wishlist.shared_with3, "shared_with3 do not match")
  
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_wishlist = resp.get_json()
        self.assertEqual(new_wishlist["name"], wishlist.name, "Names do not match")
        self.assertEqual(new_wishlist["email"], wishlist.email, "email do not match")
        self.assertEqual(new_wishlist["shared_with1"], wishlist.shared_with1, "shared_with1 do not match")
        self.assertEqual(new_wishlist["shared_with2"], wishlist.shared_with2, "shared_with2 do not match")
        self.assertEqual(new_wishlist["shared_with3"], wishlist.shared_with3, "shared_with3 do not match")

    def test_get_wishlist_by_id(self):
        """ Get a single Wishlist by id """
        # get the id of a wishlist
        test_wishlist, resp = self._create_a_wishlist()
        resp = self.app.get(
            "/wishlists/{}".format(test_wishlist["id"]), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_wishlist["name"])

    def test_delete_wishlist(self):
        """ Delete a Wishlist """
        # get the id of a wishlist
        test_wishlist, resp = self._create_a_wishlist()
        resp = self.app.delete(
            "/wishlists/{}".format(test_wishlist["id"]), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_wishlist_list(self):
        """ Get a list of Wishlist """
        self._create_wishlists(5)
        resp = self.app.get("/wishlists")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_update_wishlist(self):
        """ Update an existing wishlist """
        # create a wishlist to update
        test_wishlist = WishlistFactory()
        resp = self.app.post(
            "/wishlists", 
            json=test_wishlist.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the pet
        new_wishlist = resp.get_json()
        new_wishlist["name"] = "Updated Wishlist"
        resp = self.app.put(
            "/wishlists/{}".format(new_wishlist["id"]),
            json=new_wishlist,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_wishlist = resp.get_json()
        self.assertEqual(updated_wishlist["name"], "Updated Wishlist")

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

######################################################################
#  I T E M   T E S T   C A S E S   H E R E 
######################################################################
    def test_add_item(self):
        """ Add an item to a wishlist """
        wishlist = self._create_wishlists(1)[0]
        item = Item(
            name="DevOps Final Grade", 
            sku="A+", 
            description="Final Grade for DevOps Class", 
            quantity="5" 
        )
        resp = self.app.post(
            "/wishlists/{}/items".format(wishlist.id), 
            json=item.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["wishlist_id"], wishlist.id)
        self.assertEqual(data["name"], item.name)
        self.assertEqual(data["sku"], item.sku)
        self.assertEqual(data["description"], item.description)
        self.assertEqual(data["quantity"], item.quantity)


    def test_get_item(self):
        """ Get an item from a wishlist """
        # create a known item
        wishlist = self._create_wishlists(1)[0]
        item = Item(
            name="DevOps Final Grade", 
            sku="A+", 
            description="Final Grade for DevOps Class", 
            quantity="5" 
        )
        resp = self.app.post(
            "/wishlists/{}/items".format(wishlist.id), 
            json=item.serialize(), 
            content_type="application/json"
        )

        # retrieve it back

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]
