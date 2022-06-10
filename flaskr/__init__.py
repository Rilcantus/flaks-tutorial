import os
from flask import Flask
from numpy import True_

def create_app(test_config=None):
    # create and configure the app
    # __name__ == current Python module // helps app locate paths
    # Instance_r_c tell app files are located outiste flaskr package
    app = Flask(__name__, instance_relative_config=True)

    # sets default configurtation
    # secret = 'dev' during development, should be overridden with random num
    # DB is where the SQLite DB is saved, unduer app.i_p
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaksr.sqlite'),
    )

    # app.config.from_py overrides default values with 'config.py'
    # app.c.f_p would store real SECRET_KEY
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    # needed to ensure SQL DB file goes there
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ap simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # calls close_db and creates CLI init-db cmd
    from . import db
    db.init_app(app)

    return app