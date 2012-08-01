import hashlib
import settings

from contrib.paodate import Date
from datetime import datetime
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db


class UserPrefs(db.Model):
    """
    A data model to store per-user preferences. This stores things such as
    the username, email, when the user joined, earned awards, etc and links
    them all to a global Google account ID.
    """
    user_id = db.StringProperty()
    name = db.StringProperty()
    email = db.StringProperty()
    joined = db.DateProperty()
    awards = db.StringListProperty()
    donated = db.FloatProperty(default=0.0)

    @staticmethod
    def get():
        """
        Get or create the preferences database value for the
        currently logged in user. First try to get the object via
        memcache, falling back to the database and then updating
        memcache for the next time the object is needed.
        """
        user = users.get_current_user()

        prefs = None
        if user:
            # Attempt to fetch from memcache
            prefs = memcache.get('userprefs-' + str(user.user_id()))

            # Attempt to fetch from data store
            if not prefs:
                prefs = UserPrefs.all()\
                                 .filter('user_id =', user.user_id()).get()
                memcache.add('userprefs-' + str(user.user_id()), prefs, 3600)

            # Not found yet... time to create a new one!
            if not prefs:
                # Generate a nice username from the email
                username = user.email().split('@')[0].lower().replace(' ', '')
                count = 0

                while True:
                    check_name = count and username + str(count) or username
                    if not UserPrefs.all()\
                                    .filter('name =', check_name)\
                                    .count() and check_name not in settings.RESERVED_USERNAMES:
                        if count:
                            username = username + str(count)
                        break

                    count += 1

                # Create the preferences object and store it
                prefs = UserPrefs(**{
                    'user_id': user.user_id(),
                    'name': username,
                    'email': user.email(),
                    'joined': Date().date
                })
                prefs.put()

        return prefs

    def __repr__(self):
        """
        Return a friendly representation of this object.
        """
        return "<UserPrefs for %(name)s (%(email)s)>" % {
            'name': self.name,
            'email': self.email
        }

    def put(self, *args):
        """
        Save this object to the database, updating the memcache data as
        we do so to prevent cache misses on subsequent requests by this
        user.
        """
        super(UserPrefs, self).put(*args)

        # Update the cache, invalidating old data
        memcache.set('userprefs-' + str(self.user_id), self, 3600)

    def gravatar(self, size):
        """
        Get an avatar image link with a particular size.
        """
        hash = hashlib.md5(self.email.strip().lower()).hexdigest()
        return 'http://www.gravatar.com/avatar/%(hash)s?s=%(size)d&d=identicon' % locals()

    @property
    def gravatar_large(self):
        """
        Get an avatar image link that is 80x80px.
        """
        return self.gravatar(80)

    @property
    def gravatar_small(self):
        """
        Get an avatar image link that is 40x40px.
        """
        return self.gravatar(40)

    @property
    def recipes(self):
        """
        Get a query of recipe objects for this user.
        """
        from models.recipe import Recipe
        return Recipe.all()\
                     .filter('owner =', self)

    @property
    def brewdays(self):
        """
        Get a query of brewday objects for this user.
        TODO: Implement this.
        """
        return []