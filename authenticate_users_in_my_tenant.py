from flask import Flask, Blueprint, session, redirect, url_for
from flask_session import Session
from pathlib import Path
import config as dev_config
import os, logging

"""
Instructions for running the app:

LINUX/OSX - in a terminal window, type the following:
=======================================================
    export FLASK_APP=authenticate_users_in_my_tenant.py
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    flask run

WINDOWS - in a command window, type the following:
====================================================
    set FLASK_APP=authenticate_users_in_my_tenant.py
    set FLASK_ENV=development
    set FLASK_DEBUG=1
    flask run

You can also use "python -m flask run" instead of "flask run"
"""

def create_app(name='authenticate_users_in_my_org', root_path=Path(__file__).parent, config_dict=None):
    app = Flask(name, root_path=root_path)
    app.logger.info(f"Environment set in app.config is {app.config.get('ENV')}")
    if app.config.get('ENV') == 'production':
        app.logger.level=logging.INFO
        app.logger.error("ARE YOU SURE?")
        # if you are certain you want to run in prod,
        # supply a production config and remove this line:
        raise ValueError('This app is not meant to run in production. Run it according to instructions at top of this file.')
    elif app.config.get('ENV') == 'development':
        app.logger.level=logging.DEBUG
        app.config.from_object(dev_config)
    else:
        raise ValueError('production and development are the only options')

    if config_dict is not None:
            app.config.from_mapping(config_dict)

    # init the serverside session on the app
    Session(app)

    # We have to push the context before registering auth endpoints blueprint
    app.app_context().push()
    
    # this is where our auth-related endpoints are defined:
    import auth_endpoints
    
    # register the auth endpoints! These are:
    # sign-in status
    # token details
    # redirect
    # sign in
    # sign out
    # post sign-out
    app.register_blueprint(auth_endpoints.auth)

    # add the default route (/)
    # redirect user to page to see their sign-in status
    @app.route('/')
    def index():        
        return redirect(url_for('auth.sign_in_status'))

    return app


if __name__ == '__main__':
    root_path=Path(__file__).parent
    app=create_app(root_path=root_path)
    # the param value in the following line creates an adhoc ssl cert and allows the app to serve HTTPS on loopback (127.0.0.1).
    # Use a real certificate in production
    app.run(ssl_context='adhoc')