import urllib
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

class FoursquareCall(object):
    pass

class Foursquare(object):
    """
    A minimalist Foursquare API v2 class.

    The Foursquare v2 is structured by resources and aspects, and optional params:
    http://api.foursquare.com/v2/RESOURCE/RESOURCE_ID/ASPECT?key1=val1&...
        e.g. http://api.foursquare.com/v2/users/12345
        e.g. http://api.foursquare.com/v2/users/12345/checkins?limit=10
    See http://developer.foursquare.com for details.

    Data is available by accessing class members; the data is returned as
    normal Python data objects (lists and dictionaries).

    For example:
    fsq = Foursquare(auth) or Foursquare()
    fsq.users(id=12345)  # /users/12345
    fsq.users.friends(id=12345, limit=10)  # /users/12345/friends?limit=10

    The id parameter is the resource id; if blank, 'self' will be used.
    """
    API_BASE_URI = 'https://api.foursquare.com/v2'

    def __init__(self, auth=None, resource=None, aspect=None):
        """
        A new Foursquare API instance.
        TODO: describe params
        """
        self.auth = auth
        self.resource = resource
        self.aspect = aspect

    def __getattr__(self, m):
        try:
            return object.__getattr__(self, m)
        except AttributeError:
            if not self.resource:
                return Foursquare(auth=self.auth, resource=m)
            else:
                return Foursquare(auth=self.auth, resource=self.resource,
                                  aspect=m)

    def __call__(self, method='GET', **kwargs):
        resource_id = str(kwargs.pop('id', 'self'))
        if self.auth.token:
            kwargs['oauth_token'] = self.auth.token

        # build the url
        if self.aspect:
            uri = '%s/%s/%s/%s' % (Foursquare.API_BASE_URI, self.resource,
                                      resource_id, self.aspect)
        else:
            uri = '%s/%s/%s' % (Foursquare.API_BASE_URI, self.resource,
                                   resource_id)

        data = None
        if method == 'GET':
            uri += '?%s' % urllib.urlencode(kwargs)
        elif method == 'POST':
            data = urllib.urlencode(kwargs)
        else:
            raise KeyError('method %r not supported' % method)

        # request the data from foursquare
        # TODO: handle various exceptions here...
        # TODO: add a recorder for requests and replies for debugging
        request = urllib2.Request(uri, data=data)
        response = urllib2.urlopen(request)

        # parse response json and return
        return json.loads(response.read())
