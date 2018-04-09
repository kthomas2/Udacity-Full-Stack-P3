#!/usr/bin/python3
# Database code for the Logs Analysis project

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
sql_stmt = "select a.title, count(*)\
            from log l, articles a\
            where l.path like '%'||a.slug\
            group by a.title\
            order by 2 desc limit 3;"
title = "Most popular three articles of all time"
detail = " views"
generate_report(sql_stmt, title, detail)

# Most popular article authors of all time
sql_stmt = "select w.name, count(*)\
            from log l, articles a, authors w\
            where l.path like '%'||a.slug and a.author = w.id\
            group by w.name\
            order by 2 desc;"
title = "Most popular article authors of all time"
detail = " views"
generate_report(sql_stmt, title, detail)

# Days with more than 1% of requests lead to errors
sql_stmt = "select f.log_date, f.failed_pct\
            from failed_requests_view f\
            where f.failed_pct > 1\
            order by f.log_date desc;"
title = "Days with more than 1 % of requests lead to errors"
detail = "% errors"
generate_report(sql_stmt, title, detail)
