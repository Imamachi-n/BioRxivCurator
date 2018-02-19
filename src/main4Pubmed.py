from __future__ import print_function
from logging_utils import logger
from argparser_utils import get_argument

import access_sqlite3
from checkPubmedRSS import check_RSS
from checkAltmetrics import check_altmetrics
from sendSlackMessage import send_slack_message
from sendTwitterMessage import send_twitter_message


def main():
    # Get setting file
    setting_dict = get_argument()
    logger(__name__).info(setting_dict)

    # Parse RSS feed
    logger(__name__).info("Start Parsing RSS feed...")
    RSS_data_list = check_RSS(setting_dict['pubmed_rss_link'])

    # Create sqlite3 database if not exists
    sqlite3_file = "../db/storeAltmetrics4PubMed.sqlite3"
    if not access_sqlite3.create_tables(sqlite3_file):
        return

    # Insert new target articles into sqlite3 db
    logger(__name__).info("Insert new target articles into sqlite3 db.")
    if not access_sqlite3.insert_new_doi(sqlite3_file, RSS_data_list):
        return

    # Get all target articles for checking altmetrics score
    logger(__name__).info(
        "Get all target articles for checking altmetrics score.")
    target_doi_list = access_sqlite3.select_target_doi(sqlite3_file)

    # Get altmetric score for each article
    for doi_info in target_doi_list:
        logger(__name__).info("Get altmetric score for " + doi_info.doi)
        altmetrics_data = check_altmetrics(doi_info)
        if altmetrics_data == None:
            continue

        # Insert scores into sqlite3 db
        logger(__name__).info("Insert scores into sqlite3 db.")
        access_sqlite3.insert_altmetric_score(
            sqlite3_file, doi_info.doi, altmetrics_data)

        # Send a message to SNS
        if altmetrics_data.flg == 1:
            message = """{0}\n{1}\n""".format(doi_info.title, doi_info.url)
            send_slack_message(
                setting_dict['slack_token'],
                setting_dict['slack_channel'],
                message)

            # Tweet message
            send_twitter_message(
                setting_dict['twitter_consumer_key_pubmed'],
                setting_dict['twitter_consumer_secret_pubmed'],
                setting_dict['twitter_access_token_pubmed'],
                setting_dict['twitter_access_token_secret_pubmed'],
                message)

    logger(__name__).info("Successfully finished.")


if __name__ == '__main__':
    main()
