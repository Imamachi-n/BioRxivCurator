from __future__ import print_function
import altmetric_utils
from logging_utils import logger
from time import sleep


def checkAltmetrics(doi):
    try:
        # Get altmetric score
        sleep(1)    # Escaping hammer altmetric server
        altmetric_api = altmetric_utils.Altmetric()
        response = altmetric_api.doi(doi)

        if response:
            logger(__name__).info("Get altmetrics score for " + doi)
            # Check altmetric score (pct: >=90)
            if response["context"]['journal']['pct'] >= 90:
                flg = 1
            else:
                flg = 0
            return altmetrics_data(altmetric_score=response["score"],
                                   pct=response["context"]['journal']['pct'],
                                   flg=flg)
        else:
            logger(__name__).error(
                "Fail to getting altmetrics score for " + doi)
            return altmetrics_data(altmetric_score=0, pct=0, flg=0)

    except altmetric_utils.AltmetricHTTPException as e:
        if e.status_code == 403:
            logger(__name__).error(
                "You aren't authorized for this call.")
            logger(__name__).error(e.msg)
        elif e.status_code == 420:
            logger(__name__).error(
                "You are being rate limited.")
            logger(__name__).error(e.msg)
        elif e.status_code == 502:
            logger(__name__).error(
                "The API version you are using is currently down for maintenance.")
            logger(__name__).error(e.msg)
        elif e.status_code == 404:
            logger(__name__).error(
                "Altmetric doesn't have any details for the article or set of articles you requested.")
            logger(__name__).error(e.msg)
        return None


class altmetrics_data(object):
    def __init__(self, altmetric_score, pct, flg):
        self.altmetric_score = altmetric_score
        self.pct = pct
        self.flg = flg
