import sqlite3
from contextlib import closing
from logging_utils import logger


def create_tables(sqlite3_file):
    """
    Try to create new tables if not exists.
    :param sqlite3_file: sqlite3 database file
    :return: Boolean
    """
    try:
        with closing(sqlite3.connect(sqlite3_file)) as conn:
            c = conn.cursor()

            # Create biorxiv_altmetrics_log table
            sql = """CREATE TABLE IF NOT EXISTS biorxiv_altmetrics_log
                    (doi TEXT,
                     title TEXT,
                     link TEXT,
                     update_date TEXT,
                     altmetric_score INTEGER,
                     altmetric_pct INTEGER,
                     altmetric_flg INTEGER,
                     PRIMARY KEY(doi)
                    )"""
            c.execute(sql)
            conn.commit()

        return True

    except sqlite3.Error as e:
        logger(__name__).error(e)
        return False


def insert_new_doi(sqlite3_file, RSS_data_list):
    """
    Try to insert new doi into sqlite3 database.
    :param sqlite3_file: sqlite3 database file
    :param RSS_data_list: RSS data list
    :return: boolean
    """
    try:
        with closing(sqlite3.connect(sqlite3_file)) as conn:
            c = conn.cursor()

            # Insert article info into biorxiv_altmetrics_log if not already exists
            sql = """INSERT OR IGNORE INTO biorxiv_altmetrics_log
                     VALUES(?,?,?,?,?,?,?)"""
            doi_info = [tuple([p.doi, p.title, p.url, p.date, 0, 0, 0])
                        for p in RSS_data_list]
            c.executemany(sql, doi_info)
            conn.commit()

        return True

    except sqlite3.Error as e:
        logger(__name__).error(e)
        return False


def select_target_doi(sqlite3_file):
    """
    try to select target doi from biorxiv_altmetrics_log.
    :param sqlite3_file: sqlite3 database file
    :return: target doi list
    """
    try:
        with closing(sqlite3.connect(sqlite3_file)) as conn:
            c = conn.cursor()

            # Select target doi from biorxiv_altmetrics_log
            sql = """SELECT doi, title, link from biorxiv_altmetrics_log
                     WHERE altmetric_flg = 0"""
            c.execute(sql)

            # Store doi data as target_doi_data object
            target_doi_list = []
            for doi_info in c.fetchall():
                target_doi_list.append(target_doi_data(
                    doi=doi_info[0], title=doi_info[1], url=doi_info[2]))

        return target_doi_list

    except sqlite3.Error as e:
        logger(__name__).error(e)
        return []


def insert_altmetric_score(sqlite3_file, doi, altmetrics_data):
    """
    Try to insert altmetric score into biorxiv_altmetrics_log
    :param sqlite3_file: sqlite3 database file
    :return: boolean
    """
    try:
        with closing(sqlite3.connect(sqlite3_file)) as conn:
            c = conn.cursor()

            # insert altmetric score into biorxiv_altmetrics_log
            sql = """UPDATE biorxiv_altmetrics_log
                     SET altmetric_score = ?,
                          altmetric_pct = ?,
                          altmetric_flg = ?
                     WHERE doi = ?"""
            c.execute(sql, tuple([altmetrics_data.altmetric_score,
                                  altmetrics_data.pct, altmetrics_data.flg,
                                  doi]))
            conn.commit()

        return True

    except sqlite3.Error as e:
        logger(__name__).error(e)
        return False


class target_doi_data(object):
    def __init__(self, doi, title, url):
        self.doi = doi
        self.title = title
        self.url = url
