from flask import Flask, Blueprint, redirect, url_for, request, session, render_template, flash, g, current_app
import uuid
import msal
import json

config = current_app.config

auth = Blueprint('auth', __name__, url_prefix=config.get('AUTH_ENDPOINTS_PREFIX'), static_folder='static')

msal_instance = msal.ConfidentialClientApplication(
    config.get('CLIENT_ID'),
    client_credential=config.get('CLIENT_SECRET'),
    authority=config.get('AUTHORITY'),
    token_cache=None # we don't need a serializable token cache for this project. In-memory token cache will suffice.
)

@auth.route('/sign_in_status')
def sign_in_status():
    return render_template('auth/status.html')

@auth.route('/token_details')
def token_details():
    if session.get('msal_authenticated') != True:
        current_app.logger.info("token_details: user is not authenticated, will display 401 error")
        return render_template('auth/401.html')
    current_app.logger.info("token_details: user is authenticated, will display token details")
    return render_template('auth/token.html')

@auth.route(config.get('SIGN_IN_ENDPOINT'))
def sign_in():
    current_app.logger.info("sign_in: request received at sign in endpoint. will redirect browser to Azure AD login")
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
    current_app.logger.info("authorization_redirect: request received at redirect endpoint")
    # CSRF protection: make sure to check that state matches the one we placed in session
    # This check ensures our app + the same user session made the /authorize request that resulted in this auth code redirect
    state = session.get("state", None)
    if state is None or request.args.get('state') != state:
        current_app.logger.error("authorization redirect: state doesn't match. aborting.")
        return redirect(url_for('index'))

    if 'error' in request.args:
        current_app.logger.error("authorization_redirect: AuthN / AuthZ failed: auth code request resulted in error. aborting.")
        return redirect(url_for('index'))

    authorization_code = request.args.get('code', None)
    if authorization_code is None:
        current_app.logger.error("authorization_redirect: request to this endpoint must have 'code' URL query parameter")
        return "Bad Request: request must have 'code' URL query parameter", 400
    else:
        # we have an authorization code and have excluded common errors.
        # now we will exchange it for our tokens.
        current_app.logger.info("authorization_redirect: attempting to get a token from the /token endpoint")
        token_acquisition_result = msal_instance.acquire_token_by_authorization_code(authorization_code, config.get('SCOPES'))
        if "error" not in token_acquisition_result:
            # now we will place the token(s) and a boolean 'msal_authenticated = True' into the session for later use:
            current_app.logger.info("authorization_redirect: successfully obtained a token from the /token endpoint.\nresults are:\n")
            current_app.logger.debug(json.dumps(token_acquisition_result, indent=4, sort_keys=True))
            _place_token_details_in_session(token_acquisition_result)
        else:
            current_app.logger.error("AuthN / AuthZ failed: token request resulted in error")
            current_app.logger.error(f"{token_acquisition_result['error']}: {token_acquisition_result.get('error_description')}")

    return redirect(url_for('index'))

def _place_token_details_in_session(token_acquisition_result):
    session['msal_token_result']=token_acquisition_result
    session['msal_authenticated']=True
    id_token_claims=token_acquisition_result.get('id_token_claims', {})
    session['msal_id_token_claims'] = id_token_claims
    session['msal_username'] = id_token_claims.get('name', None)
    

@auth.route(config.get('SIGN_OUT_ENDPOINT'))
def sign_out():
    current_app.logger.info(f"sign_out: signing out user. username: {session.get('msal_username', None)}")
    return redirect(config.get('AAD_SIGN_OUT_URL'))    # send the user to Azure AD logout endpoint

@auth.route(config.get('POST_SIGN_OUT_ENDPOINT'))
def post_sign_out():
    current_app.logger.info(f"post_sign_out: clearing session for user. username: {session.get('msal_username', None)}")
    session.clear()                              # clear our server-side session on successful logout
    return redirect(url_for('index'))            # take us back to the home page
