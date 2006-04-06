from Acquisition import aq_inner
from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList
from zope.interface import implements
from zope.event import notify
from zope.app.annotation.interfaces import IAnnotations
from contentratings.interfaces import IEditorialRating
from contentratings.interfaces import IUserRating
from contentratings.events import ObjectUserRatedEvent
from contentratings.events import ObjectEditorRatedEvent

SINGLEKEY = "contentrating.singlerating"
USERKEY = "contentrating.userrating"

class EditorialRating(object):
    implements(IEditorialRating)

    annotation_key = SINGLEKEY
    scale = 5

    def __init__(self, context):
        key = self.annotation_key
        self.context = context
        self.annotations = IAnnotations(context)
        rating = self.annotations.get(key, None)
        if rating is None:
            rating = self.annotations[key] = None

    def _setRating(self, rating):
        self.annotations[self.annotation_key] = float(rating)
        notify(ObjectEditorRatedEvent(aq_inner(self.context)))

    def _getRating(self):
        return self.annotations[self.annotation_key]
    rating = property(fget=_getRating, fset=_setRating)


class UserRating(object):
    implements(IUserRating)

    annotation_key = USERKEY
    scale = 5

    def __init__(self, context):
        key = self.annotation_key
        self.context = context
        annotations = IAnnotations(context)
        mapping = annotations.get(key, None)
        ratings = OOBTree()
        anon_ratings = PersistentList()
        if mapping is None:
            blank = {'average': 0.0,
                     'ratings': ratings,
                     'anon_ratings': PersistentList(),
                     'anon_average': 0.0}
            mapping = annotations[key] = OOBTree(blank)
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
        notify(ObjectUserRatedEvent(aq_inner(self.context)))

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