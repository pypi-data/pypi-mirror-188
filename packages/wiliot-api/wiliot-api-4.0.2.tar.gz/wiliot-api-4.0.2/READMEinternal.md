# PyWiliot: wiliot-api #

wiliot-api is a python library for accessing Wiliot's cloud services from Python

## Private Library

### Installing pyWiliot - Using SSH (For Internal Use only)
generate ssh key and load the public key to [bitbucket.com](https://bitbucket.org/account/settings/ssh-keys/) for your computer
(for more details please see [Set SSH - Bitbucket Support](https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/))

then, run the following command:
````commandline
pip install git+ssh://git@bitbucket.org/wiliot/wiliot-api.git@master#egg=wiliot-api --upgrade
````

### Installing pyWiliot - Using Bitbucket user (For Internal Use only)
run the following command:
````commandline
pip install git+https://<your bitbucket ID>@bitbucket.org/wiliot/wiliot-api.git@master#egg=wiliot-api --upgrade
````
** *you can find your Bitbucket ID under ‘Your profile and setting’ > Workspace settings> Workspace ID* **

if a password is required after running the above line, generate an app password in your Bitbucket according to: 
[App passwords - Bitbucket Support](https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/), 
and use this password to install the package

See the following images for a quick-password-generation-instructions:

![installation screen 1](wiliot_api/internal/images/installation1.png)
![installation screen 2](wiliot_api/internal/images/installation2.png)
