"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Wishlist, Item, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    # return  "Reminder: return some useful information in json format about the service here", status.HTTP_200_OK
    return app.send_static_file('index.html')

######################################################################
# ADD A NEW WISHLIST
######################################################################
@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """
    Creates a wishlist
    This endpoint will create a wishlist based the data in the body that is posted
    """
    app.logger.info("Request to create a wishlist")
    check_content_type("application/json")
    wishlist = Wishlist()
    wishlist.deserialize(request.get_json())
    wishlist.create()
    message = wishlist.serialize()
    location_url = url_for("get_wishlists", wishlist_id=wishlist.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# RETRIEVE A WISHLIST by ID
######################################################################
@app.route("/wishlists/<wishlist_id>", methods=["GET"])
def get_wishlists(wishlist_id):
    """
    Retrieve a single Wishlist
    This endpoint will return a Wishlist based on it's id
    """
    app.logger.info("Request to retrieve a Wishlist with id: %s", wishlist_id)
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        raise NotFound("Wishlist with id '{}' was not found.".format(wishlist_id))
    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE A WISHLIST
######################################################################
@app.route("/wishlists/<wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    """
    Delete a Wishlist
    This endpoint will delete a Wishlist based the id specified in the path
    """
    app.logger.info("Request to delete wishlist with id: %s", wishlist_id)
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        wishlist.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# UPDATE AN EXISTING Wishlist
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlists(wishlist_id):
    """
    Update a wishlist
    This endpoint will update a wishlist based the body that is posted
    """
    app.logger.info("Request to update wishlist with id: %s", wishlist_id)
    check_content_type("application/json")
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        raise NotFound("Wishlist with id '{}' was not found.".format(wishlist_id))
    wishlist.deserialize(request.get_json())
    wishlist.id = wishlist_id
    wishlist.save()
    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)

######################################################################
# LIST ALL Wishlists (or query by name / email)
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """ Returns all of the Whishlists """
    app.logger.info("Request for wishlists")
    wishlists = []
    # e.g., /wishlists?email=rudi@isawesome.com
    email = request.args.get("email")
    # e.g., /wishlists?name=rudi
    name = request.args.get("name")
    if name:
        wishlists = Wishlist.find_by_name(name)
    elif email:
        wishlists = Wishlist.find_by_email(email)
    else:
        wishlists = Wishlist.all()

    results = [wishlist.serialize() for wishlist in wishlists]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# SHARE A WISHTLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/shared", methods=["PUT"])
def share_wishlist(wishlist_id):
    """
    Switch the "share" status of a wishlist from 0 to 1
    """
    app.logger.info("Request to share wishlist with id: %s", wishlist_id)
    check_content_type("application/json")
    wishlist = Wishlist.find_or_404(wishlist_id)
    wishlist.shared = not wishlist.shared
    wishlist.save()
    message = wishlist.serialize()
    return make_response(jsonify(message), status.HTTP_200_OK)

######################################################################
# DELETE ALL WISHLIST DATA (for testing only)
######################################################################
@app.route('/wishlists/reset', methods=['DELETE'])
def wishlists_reset():
    """ Removes all wishlists from the database """
    Wishlist.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------
#                I T E M   M E T H O D S
#---------------------------------------------------------------------

######################################################################
# ADD AN ITEM TO WISHLIST
######################################################################

@app.route('/wishlists/<int:wishlist_id>/items', methods=['POST'])
def create_items(wishlist_id):
    """
    Create an item in a Wishlist

    This endpoint will add an item to a wishlist
    """
    app.logger.info("Request to add an item to the wishlist")
    check_content_type("application/json")
    wishlist = Wishlist.find_or_404(wishlist_id)
    item = Item()
    item.deserialize(request.get_json())
    wishlist.items.append(item)
    wishlist.save()
    message = item.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)

######################################################################
# RETRIEVE AN ITEM FROM WISHLIST
######################################################################
@app.route('/wishlists/<int:wishlist_id>/items/<int:item_id>', methods=['GET'])
def get_items(wishlist_id, item_id):
    """
    Get an item
    This endpoint returns just an item
    """
    app.logger.info("Request to get an item with id: %s", item_id)
    item = Item.find_or_404(item_id)
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)

######################################################################
# UPDATE AN ITEM
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["PUT"])
def update_items(wishlist_id, item_id):
    """
    Update an Item
    This endpoint will update an item
    """
    app.logger.info("Request to update item with id: %s", item_id)
    check_content_type("application/json")
    item = Item.find_or_404(item_id)
    item.deserialize(request.get_json())
    item.id = item_id
    
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE AN ITEM
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["DELETE"])
def delete_item(wishlist_id, item_id):
    """
    Delete an Item
    This endpoint will delete an Item based the id specified in the path
    """
    app.logger.info("Request to delete item with id: %s", item_id)
    item = Item.find(item_id)
    if item:
        item.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# LIST ITEMS OR QUERY BY NAME
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["GET"])
def list_items(wishlist_id):
    """ Returns all of the items in a wishlist """
    app.logger.info("Request for wishlist items...")
    wishlist = Wishlist.find_or_404(wishlist_id)
    results = []
    name=request.args.get("name")
    if name:
        for item in wishlist.items:
            if item.name == name:
                results.append(item.serialize())
    else: results = [item.serialize() for item in wishlist.items]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Wishlist.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))