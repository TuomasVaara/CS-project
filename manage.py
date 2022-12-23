#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import sqlite3

SERVER_DIR = 'src'

# Workaround to deal with TMC inability to handle binary database files
# recreate the database file from a text dump
if os.path.exists(SERVER_DIR + '/db.sql') and not os.path.exists(SERVER_DIR + '/db.sqlite3'):
	print("Found db.sql but not db.sqlite, recreating a database")
	dump = '\n'.join(open(SERVER_DIR + '/db.sql').readlines())
	conn = sqlite3.connect(SERVER_DIR + '/db.sqlite3')
	cursor = conn.cursor()
	cursor.executescript(dump)
	conn.commit()


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SERVER_DIR + '.config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
