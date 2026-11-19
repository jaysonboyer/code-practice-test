"""Load a test-data file into the products table: python seed.py <file>"""
import os
import sys

import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])
with conn, conn.cursor() as cur:  # one transaction: commits if all succeeds
    cur.execute("truncate products")  # so re-running doesn't hit duplicate keys
    sql = open(sys.argv[1]).read()
    if sql.strip():  # an empty file means an empty table; psycopg2 rejects an empty query
        cur.execute(sql)
    cur.execute("select count(*) from products")
    print(f"Seeded {cur.fetchone()[0]} products from {sys.argv[1]}")
conn.close()
