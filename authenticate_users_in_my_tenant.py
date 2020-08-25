from flask import Flask, Blueprint, session, render_template
from flask_session import Session
from pathlib import Path
import config as dev_config
import os


def create_app(name='authenticate_users_in_my_org', root_path=Path(__file__).parent, config_dict=None):
    app = Flask(name, root_path=root_path)
    app.config['ENV'] = os.environ.get('FLASK_ENV', 'development')
    if app.config.get('ENV') == 'production':
        # supply a production config here?
        return None
    else:
        app.config['DEBUG'] = True
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
        return render_template('auth/status.html')

    return app


if __name__ == '__main__':
    root_path=Path(__file__).parent
    app=create_app(root_path=root_path)
    # the param value in the following line creates an adhoc ssl cert and allows the app to serve HTTPS on loopback (127.0.0.1).
    # Use a real certificate in production
    app.run(ssl_context='adhoc')