from flask import Flask, Blueprint, redirect, url_for, request, session, render_template, flash, g, current_app
import uuid
from pathlib import Path
import json
import msal

config = current_app.config

auth = Blueprint('auth', __name__, url_prefix=config.get('AUTH_ENDPOINTS_PREFIX'), static_folder='static')

msal_instance = msal.ConfidentialClientApplication(
    config.get('CLIENT_ID'),
    client_credential=config.get('CLIENT_SECRET'),
    authority=config.get('AUTHORITY'),
    token_cache=None # we don't really need a token cache since this is just authentication - we do not require AT or RT persistence
)

@auth.route('/token-details')
def token_details():
    return render_template('i_oidc_my_org/content.html')

@auth.route('/login')
def login():
    # state is important to check if we are receiving the code or token for the correct person (CSRF protection)
    session["state"] = str(uuid.uuid4())
    auth_url = msal_instance.get_authorization_request_url(
            config.get('SCOPES'),
            state=session.get("state", None),
            redirect_uri=config.get('REDIRECT_URI'),
            response_type=config.get('RESPONSE_TYPE'))
    return redirect(auth_url)

@auth.route(config.get('REDIRECT_ENDPOINT'))
def authorization_redirect():
    # TODO: move this logic
    authorization_code = request.args.get('code', None)
    if authorization_code is None:
        # You can also render your own Error page here!
        print("request to this endpoint must have 'code' URL query parameter")
        return "Bad Request: request must have 'code' URL query parameter", 400
    # CSRF protection: make sure to check that state matches the one we placed in session !
    if request.args.get('state') != session.get("state"):
        # should flash a message to the user side (CSRF protection)
        print("state doesn't match. cancelling auth.")
        return redirect(url_for('index'))
    elif 'error' in request.args: # AuthN/AuthZ failed :(
        # should flash a message user side
        print("AuthN / AuthZ failed")
        return redirect(url_for('index'))
    elif authorization_code:
        token_acquisition_result = msal_instance.acquire_token_by_authorization_code(authorization_code, config.get('SCOPES'))
        if token_acquisition_result != "error":
            print (f"TOKEN IS: ${token_acquisition_result}")
            session["at_result"] = token_acquisition_result

    return redirect(url_for('index'))

@auth.route('/logout')
def logout():
    return redirect(config.get('LOGOUT_URL'))    # send the user to Azure AD logout endpoint

@auth.route('/post_logout')
def post_logout():
    session.clear()                              # clear our server-side session on successful logout
    return redirect(url_for('index'))            # take us back to the home page