---
page_type: sample
author: idg-sam
languages:
  - python
products:
  - azure
  - azure-active-directory  
name: A Python Flask Webapp for signing-in users in your Azure AD tenant with the Microsoft Identity platform
urlFragment: ms-identity-python-flask-webapp-authentication
description: "This Sample demonstrates a Python Flask Webapp signing-in in users in your organization using Azure Active Directory"
---
# A Python Flask Webapp for logging in users in your organization with the Microsoft Identity platform

- [A Python Flask Webapp for logging in users in your organization with the Microsoft Identity platform](#a-python-flask-webapp-for-logging-in-users-in-your-organization-with-the-microsoft-identity-platform)
  - [Overview](#overview)
  - [Scenario](#scenario)
  - [Contents](#contents)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Step 1: Clone or download this repository](#step-1-clone-or-download-this-repository)
    - [Step 2: Install project dependencies](#step-2-install-project-dependencies)
  - [Register the sample application(s) with your Azure Active Directory tenant](#register-the-sample-applications-with-your-azure-active-directory-tenant)
    - [Choose the Azure AD tenant where you want to create your applications](#choose-the-azure-ad-tenant-where-you-want-to-create-your-applications)
      - [Register the webApp app (WebApp-MyOrg-Python)](#register-the-webapp-app-webapp-myorg-python)
      - [Configure the webApp app (WebApp-MyOrg-Python) to use your app registration](#configure-the-webapp-app-webapp-myorg-python-to-use-your-app-registration)
  - [Running the sample](#running-the-sample)
  - [Explore the sample](#explore-the-sample)
  - [About the code](#about-the-code)
  - [More information](#more-information)
  - [Community Help and Support](#community-help-and-support)
  - [Contributing](#contributing)
  - [Code of Conduct](#code-of-conduct)

![Build badge](https://identitydivision.visualstudio.com/_apis/public/build/definitions/a7934fdd-dcde-4492-a406-7fad6ac00e17/<BuildNumber>/badge)

## Overview

This Sample demonstrates a Python Flask Webapp signing-in in users in your own tenant using Azure Active Directory. The sample achieves the same using the [Microsoft Authentication Library \(MSAL\) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python).

1. The ID token is used to authenticate the user and log them in to the webapp, maintaining their logged-in status in the app session.

![Overview](./ReadmeFiles/sign-in.png)

## Scenario

- This sample shows how to build a Flask Web app that uses OpenID Connect to sign in users in an Azure AD tenant.
- Users can only sign-in with their work and school accounts in their own Azure AD tenant.



## Contents

| File/folder       | Description                                |
|-------------------|--------------------------------------------|
|`AppCreationScripts/`| Folder contains scripts to automatically configure Azure AD app registrations|
|`i_oidc_my_org.py` | The sample app code.                       |
|`auth_endpoints.py`| The auth related endpoints code.           |
| `CHANGELOG.md`    | List of changes to the sample.             |
| `CONTRIBUTING.md` | Guidelines for contributing to the sample. |
| `LICENSE`         | The license for the sample.                |

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- A virtual environment to install packages from [requirements.txt](requirements.txt)
- An Azure Active Directory (Azure AD) tenant. For more information on how to get an Azure AD tenant, see [How to get an Azure AD tenant](https://azure.microsoft.com/documentation/articles/active-directory-howto-tenant/)
- A user account in your Azure AD tenant. This sample will not work with a **personal Microsoft account**. Therefore, if you signed in to the [Azure portal](https://portal.azure.com) with a personal account and have never created a user account in your directory before, you need to do that now.

## Setup

### Step 1: Clone or download this repository

From your shell or command line:

```console
git clone https://github.com/Azure-Samples/ms-identity-python-flask-webapp-authentication.git
```

or download and extract the repository .zip file.

### Step 2: Install project dependencies

- navigate to the project folder
- activate a Python 3 virtual environment
- use the command `pip install -r requirements.txt` to install project dependencies

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


#### Register the webApp app (WebApp-MyOrg-Python)

1. Navigate to the Microsoft identity platform for developers [App registrations](https://go.microsoft.com/fwlink/?linkid=2083908) page.
1. Select **New registration**.
1. In the **Register an application page** that appears, enter your application's registration information:
   - In the **Name** section, enter a meaningful application name that will be displayed to users of the app, for example `WebApp-MyOrg-Python`.
   - Under **Supported account types**, select **Accounts in this organizational directory only**.
   - In the **Redirect URI (optional)** section, select **Web** in the combo-box and enter the following redirect URI: `http://localhost:5000/auth/redirect`.
1. Select **Register** to create the application.
1. In the app's registration screen, find and note the **Application (client) ID**. You use this value in your app's configuration file(s) later in your code.

1. Select **Save** to save your changes.

1. In the app's registration screen, click on the **Certificates & secrets** blade in the left to open the page where we can generate secrets and upload certificates.
1. In the **Client secrets** section, click on **New client secret**:
   - Type a key description (for instance `app secret`),
   - Select one of the available key durations (**In 1 year**, **In 2 years**, or **Never Expires**) as per your security concerns.
   - The generated key value will be displayed when you click the **Add** button. Copy the generated value for use in the steps later.
   - You'll need this key later in your code's configuration files. This key value will not be displayed again, and is not retrievable by any other means, so make sure to note it from the Azure portal before navigating to any other screen or blade.

#### Configure the webApp app (WebApp-MyOrg-Python) to use your app registration

Open the project in your IDE to configure the code.

> In the steps below, "ClientID" is the same as "Application ID" or "AppId".

1. Open the `config.py` file
1. Find the app key `default-value-enter-your-tenant-id-here` and replace the existing value with your Azure AD tenant ID.
1. Find the app key `default-value-enter-your-client-id-here` and replace the existing value with the application ID (clientId) of the `WebApp-MyOrg-Python` application copied from the Azure portal.
1. Find the app key `default-value-enter-your-client-secret-here` and replace the existing value with the key you saved during the creation of the `WebApp-MyOrg-Python` app, in the Azure portal.

## Running the sample

- To run the sample, navigate to the root of the project and run the command `python3 i_oidc_my_org.py`
- Navigate to `http://localhost:5000` in your browser

![Experience](./ReadmeFiles/app.png)

## Explore the sample

- Note the logged in or logged out status displayed at the center of the screen.
- Click the context-sensitive button at the top right (it should say `Login` on first run)
- Follow the instructions on the next page log in with an account in the Azure AD tenant.
- Note the context-sensitive button now says `Logout` and displays your username to its left.
- Try signing-out out!

> :information_source: Did the sample not work for you as expected? Did you encounter issues trying this sample? Then please reach out to us using the [GitHub Issues](../issues) page.

## About the code

This sample shows how to use [Microsoft Authentication Library \(MSAL\) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python) to sign-in users from an Azure AD tenant. The library is instantiated in the **auth_endpoints.py** file. The following parameters need to be provided:

* the Client ID of the app, and
* the tenant ID where the app is registered
* the Azure AD authority.
 
These values are read from the **config.py** file. MSAL Python takes care of:

 1. Downloading the Azure AD metadata, finding the signing keys, and finding the issuer name for the tenant.
 1. Processing OpenID Connect sign-in responses by validating the signature and issuer in an incoming JWT, extracting the user's claims, and putting the claims in `session['auth_current_user']['id_token_claims']` in a server-side session.

## More information

- [Microsoft Authentication Library \(MSAL\) for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python)
- [MSAL Python ReadTheDocs](https://msal-python.readthedocs.io/en/latest/)
- [Microsoft identity platform (Azure Active Directory for developers)](https://docs.microsoft.com/azure/active-directory/develop/)
- [Quickstart: Register an application with the Microsoft identity platform (Preview)](https://docs.microsoft.com/azure/active-directory/develop/quickstart-register-app)

- [Understanding Azure AD application consent experiences](https://docs.microsoft.com/azure/active-directory/develop/application-consent-experience)
- [Understand user and admin consent](https://docs.microsoft.com/azure/active-directory/develop/howto-convert-app-to-be-multi-tenant#understand-user-and-admin-consent)
- [MSAL code samples](https://docs.microsoft.com/azure/active-directory/develop/sample-v2-code)

## Community Help and Support

Use [Stack Overflow](http://stackoverflow.com/questions/tagged/msal) to get support from the community.
Ask your questions on Stack Overflow first and browse existing issues to see if someone has asked your question before.
Make sure that your questions or comments are tagged with [`azure-active-directory` `ms-identity` `adal` `msal`].

If you find a bug in the sample, please raise the issue on [GitHub Issues](../../issues).

To provide a recommendation, visit the following [User Voice page](https://feedback.azure.com/forums/169401-azure-active-directory).

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

## Code of Conduct

This project has adopted the Microsoft Open Source Code of Conduct. For more information see the Code of Conduct FAQ or contact opencode@microsoft.com with any additional questions or comments.
