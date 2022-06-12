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

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # pulls user from database where user name matches
        # fetchone is a single result
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        
        # check_p_h hashes password and checked against stored for user
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        # session stores data across requests, stored as cookies
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html')

# before_a_r runs before the view functions
# checks stored data for user_id, and pulls from database
# stores pulled info in g.user, else None
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# wraps originals view, checks user or sends to login
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view