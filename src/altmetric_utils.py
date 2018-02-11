# Altmetric API Wrapper
# Source: https://github.com/lnielsen/python-altmetric

import requests

try:
    import json
except ImportError:
    import simplejson as json


class AltmetricException(Exception):
    pass


class AltmetricHTTPException(AltmetricException):
    def __init__(self, status_code, msg):
        self.status_code = status_code
        self.msg = msg


class ParseException(AltmetricException):
    pass


class Altmetric(object):
    def __init__(self, apikey='', apiver='v1'):
        """
        Cache API key and address.
        """
        self.apikey = apikey
        self.apiver = apiver
        self.default_params = {}

        if self.apikey:
            self.default_params = {'key': apikey}

        self.api_url = "https://api.altmetric.com/{0}".format(self.apiver)

    def __repr__(self):
        if self.apikey:
            return '<Altmetric {0}: {1}>'.format(self.apiver, self.apikey)
        else:
            return '<Altmetric {0}>'.format(self.apiver)

    def call(self, method, *args, **kwargs):
        url = "{0}/{1}/{2}".format(self.api_url,
                                   method, "/".join([a for a in args]))
        # Parameter
        params = kwargs or {}
        params.update(self.default_params)

        headers = {}

        # GET request
        req = requests.get(url, params=params, headers=headers)

        # Success
        if req.status_code == 200:
            try:
                return json.loads(req.text)
            except ValueError as e:
                raise ParseException(e.message)
        elif req.status_code == 404 and req.text == "Not Found":
            return None
        else:
            raise AltmetricHTTPException(req.status_code, req.text)

    def __getattr__(self, method_name):
        def get(self, *args, **kwargs):
            return self.call(method_name, *args, **kwargs)
        return get.__get__(self)
