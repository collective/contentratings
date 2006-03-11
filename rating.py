from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList
from zope.interface import implements
from zope.app.annotation.interfaces import IAnnotations
from contentratings.interfaces import IEditorialRating
from contentratings.interfaces import IUserRating

SINGLEKEY = "contentrating.singlerating"
USERKEY = "contentrating.userrating"

class EditorialRating(object):
    implements(IEditorialRating)

    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context)
        rating = self.annotations.get(SINGLEKEY, None)
        if rating is None:
            rating = self.annotations[SINGLEKEY] = None

    def _setRating(self, rating):
        self.annotations[SINGLEKEY] = float(rating)
    def _getRating(self):
        return self.annotations[SINGLEKEY]
    rating = property(fget=_getRating, fset=_setRating)


class UserRating(object):
    implements(IUserRating)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        mapping = annotations.get(USERKEY, None)
        ratings = OOBTree()
        anon_ratings = PersistentList()
        if mapping is None:
            blank = {'average': 0.0,
                     'ratings': ratings,
                     'anon_ratings': PersistentList(),
                     'anon_average': 0.0}
            mapping = annotations[USERKEY] = OOBTree(blank)
        self.mapping = mapping

    def rate(self, rating, username=None):
        ratings = self.mapping['ratings']
        anon_ratings = self.mapping['anon_ratings']
        rating = float(rating)
        if username is not None:
            ratings[username] = rating
        else:
            anon_ratings.append(rating)
            self.mapping['anon_average'] = sum(anon_ratings)/len(anon_ratings)

        self.mapping['average'] = (sum(ratings.values()) +
                       self.mapping['anon_average']*len(anon_ratings))\
                                   /(len(ratings) + len(anon_ratings))

    def _averageRating(self):
        return self.mapping['average']
    averageRating = property(_averageRating)

    def _numberOfRatings(self):
        return len(self.mapping['ratings']) + len(self.mapping['anon_ratings'])
    numberOfRatings = property(_numberOfRatings)

    def userRating(self, username=None):
        if username is not None:
            return self.mapping['ratings'].get(username, None)
        else:
            if len(self.mapping['anon_ratings']):
                return self.mapping['anon_average']
            else:
                return None