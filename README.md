# Skill Template
This is a template repo which acts as a framework for developers to create your own skill endpoint on cloud functions in a much faster and efficient way.

# Prerequisites
- Python 3.x (You can build your skill in a different language as long as you pick a language supported on cloud functions)
- Cloud Functions on GCP

# Setup
## 1. Clone the template repo
```
$ git clone git@github.com:keito-fukuda/mercari-ai-shain-skills.git
```

## 2. Create  
### 2.1. Create your own repo
Create a remote repo with the naming convention `mercari-ai-shain-skills-${SKILL_NAME}`

### 2.2. Change remote URL
Using below git command change the URL for your remote git repo
```
$ git remote set-url origin ${GIT_URL}
```
reference: https://docs.github.com/en/github/using-git/changing-a-remotes-url

### 2.3. Verify remote URL
Verify that the remote URL has changed to new `GIT_URL` using below git command
```
$ git remote -v
```
### 2.4. Push remote repo
```
git push origin master
```

## 3. Create a Virtual Environment
```
$ python -m virtualenv venv 
```

## 4. Install Packages
```
$ pip install -r requirements.txt
```

# Project Structure
## 1. Dependencies - requirements.txt
Manage required packages with requirements.txt. 

## 2. Logic - main.py
Logics to handle your skill must be included in `main.py`

## 3. Environment Variables - .env.template.yaml
Lists all environment variables required for your skill in `.env.template.yaml` file
```
$ cp .env.template.yaml .env.yaml
```
And add the corresponding environment variable values in `.env.yaml`

## 4. Locales - locales
Multi-lingual support for your service has been performed by including required locale files under `locales` directory
For instance,
Add `ja.yaml` file which includes messages in Japanese
Add `en.yaml` file which includes messages in English
As of today, HISASHI supports only `Japanese` & `English`.

# Deployment
```
$ gcloud config set project ${GCP_PROJECT_NAME}
$ gcloud functions deploy ${FUNCTION_NAME} --trigger-http --env-vars-file .env.yaml --runtime python37 --allow-unauthenticated --entry-point main
$ gcloud functions describe ${FUNCTION_NAME} // Get a Target URL
```
*Eliminate `--env-vars-file` option if you do not need environment variables or leave the `.env.yaml` empty otherwise you will get an error on deployment.

After a successful deployment of your `skill` on `cloud functions`, you need to share the `Target URL` for your endpoint on cloud functions with the AI Shain team(#pj-ai-shain-support) so that they can configure `HISASHI` to forward the requests to your endpoint.

# Logs
```
$ gcloud functions logs read ${FUNCTION_NAME}
```

# API Specification
Webhook api request
```
method   POST
url      Target URL (url to access your skill service) 
```

`payload` should be a string representing valid JSON.

Currently there exists 2 types of payload request

1. Slack User query and Interactive component event:

`parameters`:
- user `(String)`: Slack user id (Unique)
- user_name `(String)`: Slack user name
- user_real_name `(String)`: Slack user real name
- user_phone `(String)`: Slack user contact number
- user_email `(String)`: Slack user email address
- channel_type `(String)`: Slack channel type (private/group/direct_message)
- channel `(String)`: Slack channel id (Unique)
- channel_name `(String)`: Slack channel name
- ts `(String)`: Slack event timestamp
- text `(String)`: User query in slack
- query `(String)`: User query in slack
- intent `(String)`: Dialogflow detected intent name
- confidence `(Number)`: Dialogflow confidence value
- lang `(String)`: Language code for user query
- params `(Object)`: Parameters for dialogflow detected intent
- trigger_id `(String)`: Trigger id for slack interactive component(button) click event
- intent_in_thread `(String)`: Dialogflow detected intent name in slack thread [default  value = `None`]
- is_thread `(Boolean)`: User query in slack thread or not [In thread=`True`, Not in thread=`False`]
- response_url `(String)`: Slack response url


2. Slack Dialog Submission

`parameters`:
- type `(String)`: Slack event type [type =`dialog_submission`]
- token `(String)`: Slack app token (Unique)
- team `(Object)`: Slack workspace data
    - id `(String)`: Slack team id
    - domain `(String)`: Slack domain name
- user `(Object)`: Slack user data
    - id `(String)`: Slack user id (Unique)
    - name `(String)`: Slack user name
- channel `(Object)`: Slack user data
    - id `(String)`: Slack channel id (Unique)
    - name `(String)`: Slack channel name
- submission `(Object)`: Data entered by user in slack dialog
- callback_id `(String)`: Callback id set in dialogflow intent response
- user_title `(String)`: Slack user designation/position/title
- action_ts `(String)`: Slack event timestamp
- state `(String)`: Language code for user query
- response_url `(String)`: Slack response url


# Response Format
Response format send to webhook from your skill

`response` should be a string representing valid JSON.

Currently there exists 2 types of response

1. Post slack message:

`fields`:
- slack `(Boolean)`: Response to slack or not [to slack=`True`,not to slack=`False`]
- type `(String)`: Type of response [Here value is `message`]
- message `(String)`: Message to be posted to slack 
- channel `(String)`: Slack channel id where message to be post
- thread_ts `(String)`: Timestamp for slack thread to post message in a thread

2. Open slack dialog

`fields`:
- slack `(Boolean)`: Response to slack or not [to slack=`True`,not to slack=`False`]
- type `(String)`: Type of response [Here value is `dialog`]
- dialog `(String)`: Dialog component to be opened in slack 
- channel `(String)`: Slack channel id where dialog to be open
- trigger_id `(String)`: Trigger id required to open a dialog in slack