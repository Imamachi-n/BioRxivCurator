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

            # Create doi_biorxiv_wk
            sql = """CREATE TABLE IF NOT EXISTS doi_biorxiv_wk
                    (doi TEXT, 
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

            # Check altmetric flg if not 1
            target_doi_list = []
            for doi in [tuple([p.doi, p.doi]) for p in RSS_data_list]:
                sql = """SELECT * FROM doi_biorxiv_wk 
                         WHERE doi = ? 
                         AND NOT EXISTS (SELECT * FROM biorxiv_altmetrics_log 
                                          WHERE doi = ? and altmetric_flg = 1)"""
                c.execute(sql, doi)

                # Target article if not already scored high altmetric score
                if len(c.fetchall()) > 0:
                    target_doi_list.append(str(doi[0]))

            # Insert doi into doi_biorxiv_wk table if not exists
            doi_list_for_sql = [tuple([doi]) for doi in target_doi_list]
            logger(__name__).debug(doi_list_for_sql)
            sql = "INSERT OR IGNORE INTO doi_biorxiv_wk(doi) VALUES(?)"
            c.executemany(sql, doi_list_for_sql)

            # Insert article info into biorxiv_altmetrics_log
            sql = """INSERT OR IGNORE INTO biorxiv_altmetrics_log
                     VALUES(?,?,?,?,?,?,?)"""
            doi_info = [tuple([p.doi, p.url, p.title, p.date, 0, 0, 0])
                        for p in RSS_data_list]
            c.executemany(sql, doi_info)
            conn.commit()

        return True

    except sqlite3.Error as e:
        logger(__name__).error(e)
        return False


def select_target_doi(sqlite3_file):
    """
    try to select target doi from doi_biorxiv_wk.
    :param sqlite3_file: sqlite3 database file
    :return: target doi list
    """
    try:
        with closing(sqlite3.connect(sqlite3_file)) as conn:
            c = conn.cursor()

            # Select target doi from doi_biorxiv_wk
            sql = """SELECT doi from doi_biorxiv_wk"""
            c.execute(sql)
            target_doi = [doi_tuple[0] for doi_tuple in c.fetchall()]

        return target_doi

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
