from __future__ import print_function
import feedparser
from logging_utils import logger
from HTMLParser_utils import getDOI
from datetime import datetime
from time import sleep


# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=1HYeX0emtvYhH08GonWthus8pY_vnptXA6shLd_r8lqDl-XQHp
# ((((((("Nature biotechnology"[Journal]) OR "Nature methods"[Journal]) OR "Nature genetics"[Journal]) OR "Molecular cell"[Journal]) OR "eLife"[Journal]) OR "PLoS biology"[Journal]) OR "Genome research"[Journal]) OR "Nature cell biology"[Journal]
def check_RSS(url):
    """
    Check the RSS feed of PubMed.
    - Nature biotechnology
    - Nature methods
    - Nature genetics
    - Molecular cell
    - eLife
    - PLoS biology
    - Genome research
    - Nature cell biology

    :param subjects: subject categories
    :return: RSS data list
    """
    # Get & Parse RSS
    feed = feedparser.parse(url)

    rss_data_list = []    # RSS data list object
    if feed.bozo == 1:
        logger(__name__).error(feed.bozo_exception)
        logger(__name__).error("Failed to reach the feed.")
    else:
        for pub in feed["items"]:
            link = pub["link"].split('?')[0]
            doi = getDOI(link)
            rss_data_list.append(
                RSS_data(doi=doi,
                         title=pub["title"],
                         url=link,
                         date=datetime.now().strftime("%Y-%m-%d")))
            sleep(0.5)
    return rss_data_list


class RSS_data(object):
    def __init__(self, doi, title, url, date):
        self.doi = doi
        self.title = title
        self.url = url
        self.date = date
