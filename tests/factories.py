"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Wishlist


class WishlistFactory(factory.Factory):
    """ Creates wishlists for testing """

    class Meta:
        model = Wishlist

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["Thomas", "Becca", "Bea", "Isaias", "Rudi", "John", "Rofrano"])
    email = FuzzyChoice(choices=["dog@stern.nyu.edu", "cat@stern.nyu.edu", "bird@stern.nyu.edu", "fish@stern.nyu.edu"])
    shared_with1 = FuzzyChoice(choices=["Thomas", "Becca", "Bea", "Isaias", "Rudi", "John", "Rofrano"])
    shared_with2 = FuzzyChoice(choices=["Thomas", "Becca", "Bea", "Isaias", "Rudi", "John", "Rofrano"])
    shared_with3 = FuzzyChoice(choices=["Thomas", "Becca", "Bea", "Isaias", "Rudi", "John", "Rofrano"])


if __name__ == "__main__":
    for _ in range(10):
        wishlist = WishlistFactory()
        print(wishlist.serialize())