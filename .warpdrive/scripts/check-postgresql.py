from __future__ import print_function

import os
import sys
import time
import psycopg2

host = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
dbname = os.environ['OPENSHIFT_POSTGRESQL_DB_NAME']
user = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
password = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']

remaining = 600.0
delay = 2.0

success = False

while remaining > 0.0:
    try:
        print('Check whether database is ready...')
        conn=psycopg2.connect(host=host, dbname=dbname,
                user=user, password=password)

        cursor = conn.cursor()
        cursor.execute('SELECT 1')

        success = True

        break

    except Exception:
        pass

    time.sleep(delay)

if not success:
    print('Failed to connect to database')

    sys.exit(1)
