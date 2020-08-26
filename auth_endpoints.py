from flask import Flask, Blueprint, redirect, url_for, request, session, render_template, flash, g, current_app
import uuid
import msal

config = current_app.config

auth = Blueprint('auth', __name__, url_prefix=config.get('AUTH_ENDPOINTS_PREFIX'), static_folder='static')

msal_instance = msal.ConfidentialClientApplication(
    config.get('CLIENT_ID'),
    client_credential=config.get('CLIENT_SECRET'),
    authority=config.get('AUTHORITY'),
    token_cache=None # we don't really need a token cache since this is just authentication - we do not require AT or RT persistence
)

@auth.route('/token_details')
def token_details():
    if (session.get('authenticated') != True):
        return render_template('auth/401.html')
    return render_template('auth/token.html')

@auth.route(config.get('SIGN_IN_ENDPOINT'))
def sign_in():
    # state is important since the redirect endpoint needs to know that our app + same user session initiated the process (CSRF protection)
    session["state"] = str(uuid.uuid4())
    auth_url = msal_instance.get_authorization_request_url(
            config.get('SCOPES'),
            state=session.get("state", None),
            redirect_uri=config.get('REDIRECT_URI'),
            response_type=config.get('RESPONSE_TYPE'))
    return redirect(auth_url)

@auth.route(config.get('REDIRECT_ENDPOINT'))
def authorization_redirect():
    # CSRF protection: make sure to check that state matches the one we placed in session
    # This check ensures our app + the same user session made the /authorize request that resulted in this auth code redirect
    state = session.get("state", None)
    if state is None or request.args.get('state') != state:
        current_app.logger.error("auth redirect: state doesn't match. aborting.")
        return redirect(url_for('index'))

    if 'error' in request.args:
        current_app.logger.error("AuthN / AuthZ failed: auth code request resulted in error. aborting.")
        return redirect(url_for('index'))

    authorization_code = request.args.get('code', None)
    if authorization_code is None:
        current_app.logger.error("request to this endpoint must have 'code' URL query parameter")
        return "Bad Request: request must have 'code' URL query parameter", 400
    else:
        # we have an authorization code and have excluded common errors.
        # now we will exchange it for our tokens.
        token_acquisition_result = msal_instance.acquire_token_by_authorization_code(authorization_code, config.get('SCOPES'))
        if token_acquisition_result != "error":
            current_app.logger.info(f"TOKEN IS: ${token_acquisition_result}")
            # now we will place the token(s) and a boolean 'authenticated = True' into the session for later use:
            session['msal'] = token_acquisition_result
            session['authenticated'] = True
        else:
            current_app.logger.error("AuthN / AuthZ failed: token request resulted in error")

    return redirect(url_for('index'))

@auth.route(config.get('SIGN_OUT_ENDPOINT'))
def sign_out():
    return redirect(config.get('AAD_SIGN_OUT_URL'))    # send the user to Azure AD logout endpoint

@auth.route(config.get('POST_SIGN_OUT_ENDPOINT'))
def post_sign_out():
    session.clear()                              # clear our server-side session on successful logout
    return redirect(url_for('index'))            # take us back to the home page