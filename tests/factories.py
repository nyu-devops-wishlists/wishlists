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


"""
Test Item Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Item


class ItemFactory(factory.Factory):
    """ Creates items for testing """

    class Meta:
        model = Item

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["Chocolate", "Umbrella", "Hairbrush", "Nailpolish", "Mug", "Notebook", "Carpet"])
    sku = FuzzyChoice(choices=["12345", "678910", "111213", "141516"])
    description = FuzzyChoice(choices=["darkcholocate", "pouringrain", "narsred", "ceramic", "100pages", "fur", "sturdywood"])
    quantity = FuzzyChoice(choices=["2", "12", "14", "15", "45", "100", "5000"])

if __name__ == "__main__":
    for _ in range(10):
        item = ItemFactory()
        print(item.serialize())