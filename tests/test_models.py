"""
Test cases for Wishlist Model

"""
import logging
import unittest
import os
from service.models import Wishlist, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  WISHLIST M O D E L   T E S T   C A S E S
######################################################################
class TestWishlist(unittest.TestCase):
    """ Test Cases for Wishlist Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_create_a_wishlist(self):
        """ Create a wishlist and assert that it exists """
        wishlist = Wishlist(
            name="Rudi's Wishlist",
            email="rudi@stern.nyu.edu",
            shared_with1="Becca Dailey",
            shared_with2="Thomas Chao",
            shared_with3="Isaias Martin"
        )


        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, "Rudi's Wishlist")
        self.assertEqual(wishlist.email, "rudi@stern.nyu.edu")
        self.assertEqual(wishlist.shared_with1, "Becca Dailey")
        self.assertEqual(wishlist.shared_with2, "Thomas Chao")
        self.assertEqual(wishlist.shared_with3, "Isaias Martin")


    def test_add_a_wishlist(self):
        """ Create a wishlist and add it to the database """
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = Wishlist(
            name="Rudi's Wishlist",
            email="rudi@stern.nyu.edu",
            shared_with1="Becca Dailey",
            shared_with2="Thomas Chao",
            shared_with3="Isaias Martin"
        )
        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.id, None)
        wishlist.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
    
    
    def test_find_wishlist(self):
        """ Find a Wishlist by ID """
        wishlist = Wishlist(
            name="Rudi's Wishlist",
            email="rudi@stern.nyu.edu",
            shared_with1="Becca Dailey",
            shared_with2="Thomas Chao",
            shared_with3="Isaias Martin"
        )
        wishlist.create()
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        
        expected_wishlist = wishlists[0]
        logging.debug(expected_wishlist)

        # make sure they got saved
        self.assertEqual(len(Wishlist.all()), 1)
        # find the 2nd pet in the list
        wishlist = Wishlist.find(expected_wishlist.id)
        self.assertIsNot(wishlist, None)
        self.assertEqual(wishlist.id, expected_wishlist.id)
        self.assertEqual(wishlist.name, expected_wishlist.name)
        self.assertEqual(wishlist.email, expected_wishlist.email)

    def test_find_by_name(self):
        """ Find a wishlist by Name """
        Wishlist(
            name="Rudi's Wishlist", 
            email="rudi@stern.nyu.edu", 
            shared_with1="Becca Dailey",
            shared_with2="Thomas Chao",
            shared_with3="Isaias Martin"
        ).create()
        Wishlist(
            name="Bea's Wishlist", 
            email="bea@stern.nyu.edu",
            shared_with1="Becca Dailey",
            shared_with2="Thomas Chao",
            shared_with3="Isaias Martin"
            ).create()
        wishlists = Wishlist.find_by_name("Bea's Wishlist")
        self.assertEqual(wishlists[0].email, "bea@stern.nyu.edu")
        self.assertEqual(wishlists[0].shared_with1, "Becca Dailey")
        self.assertEqual(wishlists[0].shared_with2, "Thomas Chao")
        self.assertEqual(wishlists[0].shared_with3, "Isaias Martin")
    
    def test_find_by_email(self):
        """ Find Wishlists by email """
        Wishlist(
            name="Rudi's Wishlist", 
            email="rudi@stern.nyu.edu", 
            shared_with1="Becca Dailey",
            shared_with2="Thomas Chao",
            shared_with3="Isaias Martin"
        ).create()
        Wishlist(
            name="Bea's Wishlist", 
            email="bea@stern.nyu.edu",
            shared_with1="Becca Dailey",
            shared_with2="Thomas Chao",
            shared_with3="Isaias Martin"
            ).create()
        wishlists = Wishlist.find_by_email("rudi@stern.nyu.edu")
        self.assertEqual(wishlists[0].name, "Rudi's Wishlist")
        self.assertEqual(wishlists[0].shared_with1, "Becca Dailey")
        self.assertEqual(wishlists[0].shared_with2, "Thomas Chao")
        self.assertEqual(wishlists[0].shared_with3, "Isaias Martin")

    def test_delete_a_wishlist(self):
        """ Delete a wishlist from the database """
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = Wishlist(
            name="Rudi's Wishlist",
            email="rudi@stern.nyu.edu",
            shared_with1="Becca Dailey",
            shared_with2="Thomas Chao",
            shared_with3="Isaias Martin"
            )
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        wishlist = wishlists[0]
        wishlist.delete()
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 0)