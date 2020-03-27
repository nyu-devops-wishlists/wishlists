"""
Models for Wishlist

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Wishlist(db.Model):
    """
    Class that represents a Wishlist
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    email = db.Column(db.String(32))
    shared_with1 = db.Column(db.String(63))
    shared_with2 = db.Column(db.String(63))
    shared_with3 = db.Column(db.String(63))
    items = db.relationship('Item', backref='wishlist', lazy=True)

    def __repr__(self):
        return "<Wishlist %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Wishlist to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Wishlist to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Wishlist from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Wishlist into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "shared_with1":self.shared_with1,
            "shared_with2":self.shared_with2,
            "shared_with3":self.shared_with3
        }

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            # self.id = data["id"]
            self.name = data["name"]
            self.email = data["email"]
            self.shared_with1 = data["shared_with1"]
            self.shared_with2 = data["shared_with2"]
            self.shared_with3 = data["shared_with3"]
        except KeyError as error:
            raise DataValidationError("Invalid Wishlist: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained" "bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Wishlist in the database """
        logger.info("Processing all Wishlist")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Wishlist by its ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Wishlist by its id or return 404 """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Wishlist with the given name

        Args:
            name (string): the name of the Wishlist you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
    
    @classmethod
    def find_by_id(cls, id):
        """ Returns all Wishlist with the given id

        Args:
            id (string): the id of the Wishlist you want to match
        """
        logger.info("Processing id query for %s ...", id)
        return cls.query.filter(cls.id == id)

    @classmethod
    def find_by_email(cls, email):
        """ Returns all Wishlist with the given email

        Args:
            name (string): the name of the Wishlist you want to match
        """
        logger.info("Processing name query for %s ...", email)
        return cls.query.filter(cls.email == email)

######################################################################
#  I T E M   M O D E L
######################################################################
class Item(db.Model):
    """
    Class that represents an Item
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlist.id'), nullable=False)
    name = db.Column(db.String(64)) # e.g., toothbrush, book, phone
    sku = db.Column(db.String(64))
    description = db.Column(db.String(64))
    quantity = db.Column(db.String(64))

    def __repr__(self):
        return "<Item %r id=[%s] wishlist[%s]>" % (self.name, self.id, self.wishlist_id)

    def __str__(self):
        return "%s: %s, %s, %s " % (self.name, self.sku, self.description, self.quantity)

    def serialize(self):
        """ Serializes a Address into a dictionary """
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "name": self.name,
            "sku": self.sku,
            "description": self.description,
            "quantity": self.quantity,
        }

    def deserialize(self, data):
        """
        Deserializes a Address from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.wishlist_id = data["wishlist_id"]
            self.name = data["name"]
            self.sku = data["sku"]
            self.description = data["description"]
            self.quantity = data["quantity"]
        except KeyError as error:
            raise DataValidationError("Invalid Item: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained" "bad or no data"
            )
        return self
    
    def save(self):
        """
        Updates a Wishlist to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()
    
    def delete(self):
        """ Removes a Item from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Wishlist in the database """
        logger.info("Processing all Wishlist")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Wishlist by its ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Wishlist by its id or return 404 """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Items with the given name

        Args:
            name (string): the name of the Wishlist you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
    
    @classmethod
    def find_by_id(cls, id):
        """ Returns the Item with the given id

        Args:
            id (string): the id of the Item you want to match
        """
        logger.info("Processing id query for %s ...", id)
        return cls.query.filter(cls.id == id)

    @classmethod
    def find_by_sku(cls, sku):
        """ Returns the Item with the given sku

        Args:
            sku (string): the sku of the Item you want to match
        """
        logger.info("Processing sku query for %s ...", sku)
        return cls.query.filter(cls.sku == sku)
