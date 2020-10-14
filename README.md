---
page_type: sample
languages:
  - python
  - flask
products:
  - azure
  - azure-active-directory  
name: A Python Flask Webapp for signing-in users in your Azure AD tenant with the Microsoft Identity platform
urlFragment: ms-identity-python-flask-webapp-authentication
description: "This sample demonstrates a Python Flask webapp that signs in users in your tenant using Azure Active Directory"
---
# A Python Flask Webapp for signing in users in your organization with the Microsoft identity platform

  - [Overview](#overview)
  - [Scenario](#scenario)
  - [Contents](#contents)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Step 1: Clone or download this repository](#step-1-clone-or-download-this-repository)
    - [Step 2: Install project dependencies](#step-2-install-project-dependencies)
  - [Register the sample application(s) with your Azure Active Directory tenant](#register-the-sample-applications-with-your-azure-active-directory-tenant)
    - [Choose the Azure AD tenant where you want to create your applications](#choose-the-azure-ad-tenant-where-you-want-to-create-your-applications)
      - [Register the webApp app (WebApp_Python_Flask_Authentication_MyOrg)](#register-the-webapp-app-webapp_python_flask_authentication_myorg)
      - [Configure the webApp app (WebApp_Python_Flask_Authentication_MyOrg) to use your app registration](#configure-the-webapp-app-webapp_python_flask_authentication_myorg-to-use-your-app-registration)
  - [Running the sample](#running-the-sample)
  - [Explore the sample](#explore-the-sample)
  - [About the code](#about-the-code)
  - [More information](#more-information)
  - [Community Help and Support](#community-help-and-support)
  - [Contributing](#contributing)
  - [Code of Conduct](#code-of-conduct)

<!-- ![Build badge](https://identitydivision.visualstudio.com/_apis/public/build/definitions/a7934fdd-dcde-4492-a406-7fad6ac00e17/<BuildNumber>/badge)
// TODO: COMMENT OUT BUILD BADGE UNTIL WE FIND A PURPOSE FOR IT-->
## Overview

This sample demonstrates a Python Flask web app signing-in users in your own tenant using the [Microsoft Authentication Library \(MSAL\) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python) with Azure Active Directory.

![Overview](./ReadmeFiles/sign-in.png)

## Scenario

- This sample shows how to build a Flask Web app that uses [Microsoft Authentication Library \(MSAL\) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python) leveraging the OpenID Connect protocol to sign in users in an organization's Azure Active Directory tenant.
- Users can only sign in with their work and school accounts in their own Azure AD tenant.
- Once the user has signed in with Azure AD, the ID token is used by the webapp to authenticate, maintaining the user's signed-in status in a session variable.


## Contents

| File/folder       | Description                                |
|-------------------|--------------------------------------------|
|`AppCreationScripts/`| Folder contains scripts to automatically configure Azure AD app registrations|
|`authenticate_users_in_my_tenant.py` | The sample app code.                       |
|`auth_endpoints.py`| The auth related endpoints code.           |
|`CHANGELOG.md`     | List of changes to the sample.             |
|`CONTRIBUTING.md`  | Guidelines for contributing to the sample. |
|`LICENSE`          | The license for the sample.                |

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- A virtual environment to install packages from [requirements.txt](requirements.txt)
- An Azure Active Directory (Azure AD) tenant. For more information on how to get an Azure AD tenant, see [How to get an Azure AD tenant](https://azure.microsoft.com/documentation/articles/active-directory-howto-tenant/)
- A user account in your Azure AD tenant. This sample will not work with a **personal Microsoft account**. Therefore, if you signed in to the [Azure portal](https://portal.azure.com) with a personal account and have never created a user account in your directory before, you need to do that now.

## Setup

### Step 1: Clone or download this repository

From your shell or command line:

```Shell
git clone https://github.com/Azure-Samples/ms-identity-python-flask-webapp-authentication.git
```

or download and extract the repository .zip file.

### Step 2: Install project dependencies

1. navigate to the project folder
2. activate a Python 3 virtual environment
3. install project dependencies

- In Linux/OSX via the terminal:
```Shell
  cd project-root-directory
  python3 -m venv venv # only required if you don't have a venv already
  source venv/bin/activate
  pip install -r requirements.txt
```
- In Windows via PowerShell:
```PowerShell
  cd project-root-directory
  python3 -m venv venv # only required if you don't have a venv already
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
  . .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
```

## Register the sample application(s) with your Azure Active Directory tenant

There is one project in this sample. To register it, you can:

- either follow the step [Choose the Azure AD tenant where you want to create your applications](#choose-the-azure-ad-tenant-where-you-want-to-create-your-applications) below
- or use PowerShell scripts that:
  - **automatically** creates the Azure AD applications and related objects (passwords, permissions, dependencies) for you.
  - modify the projects' configuration files.

<details>
  <summary>Expand this section if you want to use this automation:</summary>

1. On Windows, run PowerShell and navigate to the root of the cloned directory
1. In PowerShell run:

   ```PowerShell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
   ```

1. Run the script to create your Azure AD application and configure the code of the sample application accordingly.
1. In PowerShell run:

   ```PowerShell
   cd .\AppCreationScripts\
   .\Configure.ps1
   ```

   > Other ways of running the scripts are described in [App Creation Scripts](./AppCreationScripts/AppCreationScripts.md)
   > The scripts also provide a guide to automated application registration, configuration and removal which can help in your CI/CD scenarios.

</details>

Follow the steps below to manually walk through the steps to register and configure the applications in the Azure portal.

### Choose the Azure AD tenant where you want to create your applications

As a first step you'll need to:

1. Sign in to the [Azure portal](https://portal.azure.com).
1. If your account is present in more than one Azure AD tenant, select your profile at the top right corner in the menu on top of the page, and then **switch directory** to change your portal session to the desired Azure AD tenant..


#### Register the webApp app (WebApp_Python_Flask_Authentication_MyOrg)

1. Navigate to the Microsoft identity platform for developers [App registrations](https://go.microsoft.com/fwlink/?linkid=2083908) page.
1. Select **New registration**.
1. In the **Register an application page** that appears, enter your application's registration information:
   - In the **Name** section, enter a meaningful application name that will be displayed to users of the app, for example `WebApp_Python_Flask_Authentication_MyOrg`.
   - Under **Supported account types**, select **Accounts in this organizational directory only**.
   - In the **Redirect URI (optional)** section, select **Web** in the combo-box and enter the following redirect URI: `https://127.0.0.1:5000/auth/redirect`.
1. Select **Register** to create the application.
1. In the app's registration screen, find and note the **Application (client) ID**. You use this value in your app's configuration file(s) later in your code.

1. Select **Save** to save your changes.

1. In the app's registration screen, click on the **Certificates & secrets** blade in the left to open the page where we can generate secrets and upload certificates.
1. In the **Client secrets** section, click on **New client secret**:
   - Type a key description (for instance `app secret`),
   - Select one of the available key durations (**In 1 year**, **In 2 years**, or **Never Expires**) as per your security concerns.
   - The generated key value will be displayed when you click the **Add** button. Copy the generated value for use in the steps later.
   - You'll need this key later in your code's configuration files. This key value will not be displayed again, and is not retrievable by any other means, so make sure to note it from the Azure portal before navigating to any other screen or blade.

#### Configure the webApp app (WebApp_Python_Flask_Authentication_MyOrg) to use your app registration

Open the project in your IDE to configure the code.

> In the steps below, "ClientID" is the same as "Application ID" or "AppId".

1. Open the `config.py` file
1. Find the app key `default-value-enter-your-tenant-id-here` and replace the existing value with your Azure AD tenant ID.
1. Find the app key `default-value-enter-your-client-id-here` and replace the existing value with the application ID (clientId) of the `WebApp_Python_Flask_Authentication_MyOrg` application copied from the Azure portal.
1. Find the app key `default-value-enter-your-client-secret-here` and replace the existing value with the key you saved during the creation of the `WebApp_Python_Flask_Authentication_MyOrg` app, in the Azure portal.

## Running the sample

- To run the sample, open a terminal window. Navigate to the root of the project. Be sure your virtual environment with dependencies is activated ([Prerequisites](#prerequisites)). 
- In Linux/OSX via the terminal:
  ```Shell
    export FLASK_APP=authenticate_users_in_my_tenant.py
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    export FLASK_RUN_CERT=adhoc
    flask run
  ```
- In Windows via PowerShell:
  ```PowerShell
    set FLASK_APP=authenticate_users_in_my_tenant.py
    set FLASK_ENV=development
    set FLASK_DEBUG=1
    set FLASK_RUN_CERT=adhoc
    flask run
  ```
- Alternatively, you may use `python -m flask run` instead of `flask run`
- Navigate to [https://127.0.0.1:5000](https://127.0.0.1:5000) in your browser

![Experience](./ReadmeFiles/app.png)

## Explore the sample

- Note the signed-in or signed-out status displayed at the center of the screen.
- Click the context-sensitive button at the top right (it will read `Sign In` on first run)
- Follow the instructions on the next page to sign in with an account in the Azure AD tenant.
- Note the context-sensitive button now says `Sign out` and displays your username to its left.
- The middle of the screen now has an option to click for ID Token Details: click it to see some of the ID token's decoded claims.
- You can also use the button on the top right to sign out.
- After signing out, click this link to the [token details page](https://127.0.0.1:5000/auth/token_details) to observe how the app displays a `401: unauthorized` error instead of the ID token claims.

> :information_source: Did the sample not work for you as expected? Did you encounter issues trying this sample? Then please reach out to us using the [GitHub Issues](../issues) page.

## About the code

This sample shows how to use [Microsoft Authentication Library \(MSAL\) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python) to sign in users from your Azure AD tenant. 

* A **ConfidentialClientApplication** object is instantiated in the [auth_endpoints.py](auth_endpoints.py) file. The following parameters need to be provided upon instantiation:

  * The **Client ID** of the app
  * The **Azure AD Authority** (which, in this sample, includes the Tenant ID of the AAD application).
  * The **Client Secret**, which is a requirement for Confidential Client Applications

* In this sample, these values are read from the flask configuration object, which receives them from the [config.py](config.py) file. 

```python
msal_instance = msal.ConfidentialClientApplication(
    config.get('CLIENT_ID'),
    client_credential=config.get('CLIENT_SECRET'),
    authority=config.get('AUTHORITY'),
    token_cache=None # we don't need a serializable token cache for this project. In-memory token cache will suffice.
)
```
1. The first step of the sign-in process is to send a request to the /authorize endpoint on Azure Active Directory. Our MSAL(Python) ConfidentialClientApplication instance is leveraged to construct an authorization request URL, and our app redirects the browser to this URL.
1. The user is presented with a sign-in prompt by Azure Active Directory. If the sign-in attempt is successful, the user's browser is redirected to our app's redirect endpoint. A valid request to this endpoint will contain an **authorization code**.
1. Our ConfidentialClientApplication instance then exchanges this authorization code for an ID Token and Access Token from Azure Active Directory.

```python
token_acquisition_result = msal_instance.acquire_token_by_authorization_code(authorization_code, config.get('SCOPES'))
```

MSAL Python:
* Downloads the Azure AD metadata, including signing keys, and finds the issuer name for the tenant.
* Processes Azure AD responses by validating the signature and issuer in the ID and/or Access tokens.
* Parses the ID Token claims into plaintext.
 
The result is then put into a server-side session, in the following properties:
```python
session['msal_token_result']=token_acquisition_result
session['msal_authenticated']=True
id_token_claims=token_acquisition_result.get('id_token_claims', {})
session['msal_id_token_claims'] = id_token_claims
session['msal_username'] = id_token_claims.get('name', None)
```

## More information

- [Microsoft Authentication Library \(MSAL\) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python)
- [MSAL Python ReadTheDocs](https://msal-python.readthedocs.io/en/latest/)
- [Microsoft identity platform (Azure Active Directory for developers)](https://docs.microsoft.com/azure/active-directory/develop/)
- [Quickstart: Register an application with the Microsoft identity platform (Preview)](https://docs.microsoft.com/azure/active-directory/develop/quickstart-register-app)

- [Understanding Azure AD application consent experiences](https://docs.microsoft.com/azure/active-directory/develop/application-consent-experience)
- [Understand user and admin consent](https://docs.microsoft.com/azure/active-directory/develop/howto-convert-app-to-be-multi-tenant#understand-user-and-admin-consent)
- [MSAL code samples](https://docs.microsoft.com/azure/active-directory/develop/sample-v2-code)

## Community Help and Support

Use [Stack Overflow](https://stackoverflow.com/questions/tagged/msal) to get support from the community.
Ask your questions on Stack Overflow first and browse existing issues to see if someone has asked your question before.
Make sure that your questions or comments are tagged with [`azure-active-directory` `ms-identity` `adal` `msal`].

If you find a bug in the sample, please raise the issue on [GitHub Issues](../../issues).

To provide a recommendation, visit the following [User Voice page](https://feedback.azure.com/forums/169401-azure-active-directory).

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

## Code of Conduct

This project has adopted the Microsoft Open Source Code of Conduct. For more information see the Code of Conduct FAQ or contact opencode@microsoft.com with any additional questions or comments.
