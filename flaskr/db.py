import sqlite3

import click
# g unique for each req, used to store data which might be used again
# current_app points to the Flask application handling the req

from flask import current_app, g 
from  flask.cli import with_appcontext

def get_db():
    # called when application is created and is handling a request
    if 'db' not in g:
        # connects to stored DB key
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # .Row = rows returned behave like dictonarys
        # access column by name
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    # checks if handshake was made, if made then is closed
    db = g.pop('db', None)

    if db is not None:
        db.close()
