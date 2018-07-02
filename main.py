"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt

from alayatodo import app
from database import init_db
from resources.fixtures import populate_database


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        init_db()
        populate_database()
        print("AlayaTodo: Database initialized.")
    else:
        app.run(use_reloader=True)
