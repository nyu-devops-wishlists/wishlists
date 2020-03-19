"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Wishlist


class WishlistFactory(factory.Factory):
    """ Creates fake pets that you don't have to feed """

    class Meta:
        model = Wishlist

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["Pratyush", "Cata", "Kevin", "Colin", "John","Rofrano"])
    email = FuzzyChoice(choices=["dog@stern.nyu.edu", "cat@stern.nyu.edu", "bird@stern.nyu.edu", "fish@stern.nyu.edu"])
    shared_with1 = FuzzyChoice(choices=["Pratyush", "Cata", "Kevin", "Colin", "John","Rofrano"])
    shared_with2 = FuzzyChoice(choices=["Pratyush", "Cata", "Kevin", "Colin", "John","Rofrano"])
    shared_with3 = FuzzyChoice(choices=["Pratyush", "Cata", "Kevin", "Colin", "John","Rofrano"])


if __name__ == "__main__":
    for _ in range(10):
        wishlist = WishlistFactory()
        print(wishlist.serialize())