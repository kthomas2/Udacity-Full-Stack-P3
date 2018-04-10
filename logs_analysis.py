#!/usr/bin/python3
"""Database code for the Logs Analysis project."""

import psycopg2

DBNAME = "news"


def get_report_data(sql_stmt):
    """Get the report data from the news database."""
    # Open database connection
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql_stmt)
    report_data = c.fetchall()
    db.close()
    return report_data


def generate_report(sql_stmt, title, detail):
    """Generate the report."""
    data = get_report_data(sql_stmt)
    print("\n" + title + "\n")
    for row in data:
        print(" {} -- {}{}".format(row[0], row[1], detail))
    print("\n")


# Most popular three articles of all time
sql_stmt = "SELECT a.title, count(*)\
            FROM log l, articles a\
            WHERE l.path LIKE '%'||a.slug\
            GROUP BY a.title\
            ORDER BY 2 DESC LIMIT 3;"
title = "Most popular three articles of all time"
detail = " views"
generate_report(sql_stmt, title, detail)

# Most popular article authors of all time
sql_stmt = "SELECT w.name, count(*)\
            FROM log l, articles a, authors w\
            WHERE l.path LIKE '%'||a.slug AND a.author = w.id\
            GROUP BY w.name\
            ORDER BY 2 DESC;"
title = "Most popular article authors of all time"
detail = " views"
generate_report(sql_stmt, title, detail)

# Days with more than 1% of requests lead to errors
sql_stmt = "SELECT f.log_date, f.failed_pct\
            FROM failed_requests_view f\
            WHERE f.failed_pct > 1\
            ORDER BY f.log_date DESC;"
title = "Days with more than 1 % of requests lead to errors"
detail = "% errors"
generate_report(sql_stmt, title, detail)
