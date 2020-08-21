from flask import Flask, Blueprint, session, render_template
from flask_session import Session
from pathlib import Path
import json
import config as dev_config
import os


def create_app(name='i_oidc_my_org', root_path=Path(__file__).parent, config_dict=None):
    app = Flask(name, root_path=root_path)
    if os.environ.get('FLASK_ENV') == 'production':
        # supply a production config here?
        return None
    else:
        app.config.from_object(dev_config)

    if config_dict is not None:
            app.config.from_mapping(config_dict)

    # init the serverside session on the app
    Session(app)

    # We have to push the context before registering auth endpoints blueprint
    app.app_context().push()
    
    # this is where our auth-related endpoints are defined:
    import auth_endpoints
    
    # register the auth endpoints!
    app.register_blueprint(auth_endpoints.auth)

    # add the default route (/)
    @app.route('/')
    def index():
        # is there already an id token in the user's session? if not make an empty dictionary
        return render_template('i_oidc_my_org/content.html')

    return app


if __name__ == '__main__':
    root_path=Path(__file__).parent
    app=create_app(root_path=root_path)
    # the param value in the following line creates an adhoc ssl cert and allows the app to serve HTTPS on loopback 127.0.0.1.
    # Use a real certificate in production
    app.run(ssl_context='adhoc')