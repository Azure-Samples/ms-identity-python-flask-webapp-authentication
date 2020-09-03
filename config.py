import os

### YOUR APP CONFIGS ###

# this is required for encrypting flask session cookies.
SECRET_KEY = os.environ.get('SAMPLE_APP_ENCRYPTION_KEY','enter-a-great-key') # should be loaded from env vars or other secure location.
SESSION_TYPE = 'filesystem'

# Your Hosted or Local App URL. Flask runs the dev server on 127.0.0.1:5000 by default
APP_URL = 'https://127.0.0.1:5000'

# Your app's redirect URL.
REDIRECT_ENDPOINT = '/redirect'

# Auth Endpoints Prefix. This app's auth-related endpoints are under /auth
AUTH_ENDPOINTS_PREFIX = '/auth'

# your app's redirect URL
# AAD will tell the user's browser to go here after the user enters credentials
REDIRECT_URL = f'{APP_URL}{AUTH_ENDPOINTS_PREFIX}{REDIRECT_ENDPOINT}'

# Our app's sign in URL
SIGN_OUT_ENDPOINT = '/sign_in'

# Our app's sign out URL
SIGN_OUT_ENDPOINT = '/sign_out'

# AAD will redirect the user here after a successful logout.
POST_SIGN_OUT_ENDPOINT = '/post_sign_out'

# AAD will send a request here to clear out the user session after successful sign out.
POST_SIGN_OUT_URL = f'{APP_URL}{AUTH_ENDPOINTS_PREFIX}{POST_SIGN_OUT_ENDPOINT}'

# auth response type - we only want to authenticate and get an ID TOKEN in this case
RESPONSE_TYPE = 'code' # MSAL default is 'code' if this is not provided.

### AZURE ACTIVE DIRECTORY APPLICATION CONFIGS ###

# Your Azure AD tenant's ID / Directory ID on Azure AD
TENANT_ID = 'default-value-enter-your-tenant-id-here'

# Your app's client/app ID on Azure AD
CLIENT_ID = 'default-value-enter-your-client-id-here'

# Your app's client secret on Azure AD
# NEVER save this in the configs in a production system - it should be loaded from env variable, key vault, or other secure location.
CLIENT_SECRET = os.environ.get('SAMPLE_APP_CLIENT_SECRET', 'default-value-enter-your-client-secret-here')

#Scopes requested by the application
SCOPES = [] # where we're going, we don't need scopes (default scopes suffice)

### AZURE ACTIVE DIRECTORY AUTHORITY URLs ###

# The base URL of the authority through which MSAL python will try to authenticate / authorize
AUTHORITY_BASE = 'https://login.microsoftonline.com'

# This endpoint is useful when we need to authenticate / authorize a user on any AAD tenant
AUTHORITY_COMMON_ENDPOINT = "/common"

# The authority through which MSAL Python will try to authenticate / authorize in single tenant apps
AUTHORITY_SINGLE_TENANT = f'{AUTHORITY_BASE}/{TENANT_ID}' #append '/tenant-id' to the end of AUTHORITY_BASE

# The authority through which MSAL Python will try to authenticate / authorize in multi tenant apps
AUTHORITY_MULTI_TENANT = f'{AUTHORITY_BASE}{AUTHORITY_COMMON_ENDPOINT}' # append '/common' to the end of AUTHORITY_BASE

# The authority through which MSAL Python will try to authenticate / authorize in this app
AUTHORITY = AUTHORITY_SINGLE_TENANT

### AZURE ACTIVE DIRECTORY LOGOUT URLS ###

# The AAD endpoint to log your user out
AAD_SIGN_OUT_ENDPOINT = '/oauth2/v2.0/logout'

# post-logout param to tell AAD to redirect the user back to the app
AAD_POST_SIGN_OUT_URL_PARAM = f'?post_logout_redirect_uri={POST_SIGN_OUT_URL}'

# The URL for AAD to log your user out.
AAD_SIGN_OUT_URL = f'{AUTHORITY}{AAD_SIGN_OUT_ENDPOINT}{AAD_POST_SIGN_OUT_URL_PARAM}'
