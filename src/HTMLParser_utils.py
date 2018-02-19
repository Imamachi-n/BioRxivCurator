from __future__ import print_function
import feedparser
from HTMLParser import HTMLParser
import re
import requests


class parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.link = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and re.match("^//doi.org", attrs["href"]):
            self.flag = True
            self.link = attrs["href"].replace("//doi.org/", "")

    def handle_data(self, data):
        if self.flag:
            self.flag = False


def getDOI(link):
    r = requests.get(link)
    test = parser()
    test.feed(r.text)
    return test.link
