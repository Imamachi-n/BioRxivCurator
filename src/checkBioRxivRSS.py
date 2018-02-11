from __future__ import print_function
import feedparser
from logging_utils import logger


def check_RSS(*subjects):
    """
    Check the RSS feed of BioRxiv
    :param subjects: comma-separated subject categories
    :return: RSS data list
    """
    # Get & Parse RSS
    feed = feedparser.parse(
        "http://connect.biorxiv.org/biorxiv_xml.php?subject={0}".format("+".join(subjects)))

    rss_data_list = []    # RSS data list object
    if feed.bozo == 1:
        logger(__name__).error(feed.bozo_exception)
        logger(__name__).error("Failed to reach the feed.")
    else:
        for pub in feed["items"]:
            rss_data_list.append(
                RSS_data(doi=pub["dc_identifier"],
                         title=pub["title"],
                         url=pub["link"].split('?')[0],
                         date=pub["updated"]))
    return rss_data_list


class RSS_data(object):
    def __init__(self, doi, title, url, date):
        self.doi = doi
        self.title = title
        self.url = url
        self.date = date
