# YoutubeNotifier



# Prereqs

* Python 3.x
<!-- * DiscordPy -->
* Google Sheets API


## Discord Python API 

### (Recommended) Setup a pyenv
```bash
python3 -m venv bot-env
```
#### To Activate:
##### Linux:
```bash
source bot-env/bin/activate
```
##### Windows:
```bash
bot-env\Scripts\activate.bat
```
<!-- 
### Install Discord Dependencies
more info [here](https://discordpy.readthedocs.io/en/stable/intro.html)

```bash
pip install -U discord.py
``` -->

## Youtube API
### Install dependencies
more info [here](https://developers.google.com/youtube/v3/quickstart/python)

```bash
#Note: make sure your pip version is 3.x. Alternatively, use pip3. If you're using a pyenv, make sure it's activated
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
### Create your credentials.json file
more info [here](https://developers.google.com/workspace/guides/create-credentials)

1. Go to https://console.cloud.google.com/ and create a new project (or use an existing one).
1. Add `Youtube Data API v3` to your project.
1. Go to `APIs & Services` > `OAuth consent screen`
	1. Click `External` User Type, and fill in all of the required information
1. Go to `APIs & Services` > `Credentials` > `Create Credentials` > `OAuth Client ID`
	1. Fill in the required information. Once you're done, you should be brought back to the `Credentials` page.
1. Under OAuth 2.0 Client IDs, you should now have a new Client ID. Go to the right and click download.
1. rename the file to `credentials.json` and place it in the root directory of this reposity.
1. Go to `APIs & Services` > `OAuth consent screen` > `Audience` > `Test Users` and add your email as a Test User.

<!-- 
### Configuring Bot Token And SpreadSheetId

You need to setup 1 env_vars:

`BOT_TOKEN` should be your discord bot token.

Alternatively, you can create an additional files: `bottoken.txt`

`bottoken.txt` should contain your discord bot token. -->


Afterwards... simpy run :D
```bash
python notifier/youtubenotifier.py
```

Note: First time running will open up a tab, where you will need to allow permissions and get through Safety in accessing the spreadsheet. If you get one of those red warning insecure pages, you need to click `Advanced` > `Continue to page`.

Note: When running for the first time, you might also get hit with the following

`Access blocked: YoutubeNotifier has not completed the Google verification process`

In which case, you forgot to add your google account as a test user to your Google project.