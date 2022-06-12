from crypt import methods
import functools
from click import password_option

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# creates a base url Blueprint extened upon different views
bp = Blueprint('auth', __name__, url_prefix='/auth')

# route makes URL /register call register()
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # if user submitted form will return true and run below
    if request.method == 'POST':
        # request.f is special dict
        # user inputs username and password
        username = request.form['username']
        password = request.form['password']
        # start the database
        db = get_db()
        # set error to NoneType
        error = None

        # validates user entered user then password
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # if validation is successful then insert into database      
        if error is None:
            try:
                # replaces user input with ?/? placeholders
                # reduces SQL injection
                # gen_pass_hah used to store a hash of the password
                db.execute(
                    "INSERT INTO user (username, password) Values (?, ?)",
                    (username, generate_password_hash(password)),
                )
                # commits data to datebase
                db.commit()
            except db.IntegrityError:
                # check if user already exists
                error = f"User {username} is already registered."
            else:
                # redirect sends you to login view (function)
                return redirect(url_for("auth.login"))

        # if validation fails, flash stores mesages that can be used later
        flash(error)
    
    # return the html for the register view
    return render_template('auth/register.html')