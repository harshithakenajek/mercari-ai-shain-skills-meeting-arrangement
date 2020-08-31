# Skill Boilerplate
This is a repo which acts as a template for developers to create your own skill endpoint on cloud functions in a much faster and efficient way.

# Prerequisites
- Python 3.x (You can build your skill in a different language as long as you pick a language supported on cloud functions)
- Cloud Functions on GCP

If you would like to build your skill on a different platform, that's fine as long as your skill provides necessary HTTPs endpoint.
In that case, please jump to step 5 after creating your HTTPs endpoint.

# Steps
## 1. Clone the template repo
```
$ git clone git@github.com:kouzoh/mercari-ai-shain-skills-boilerplate.git
```

## 2. Create a repo for your skill 
### 2.1. Create your own repo
Create a remote repo with the naming convention `mercari-ai-shain-skills-${SKILL_NAME}`.

### 2.2. Change remote URL
Change the URL for your remote git repo and verify it.
```
$ git remote set-url origin ${GIT_URL}
$ git remote -v
```
reference: https://docs.github.com/en/github/using-git/changing-a-remotes-url

### 2.3. Push remote repo
```
git push origin master
```

## 3. Create a Virtual Environment
```
$ python3 -m venv venv
$ . venv/bin/activate
```

## 4. Install Dependencies
```
$ pip install -r requirements.txt
```

## 5. Deployment
```
$ gcloud config set project ${GCP_PROJECT_NAME}
$ gcloud functions deploy ${FUNCTION_NAME} --trigger-http --env-vars-file .env.yaml --runtime python37 --allow-unauthenticated --entry-point main
$ gcloud functions describe ${FUNCTION_NAME} // Get a Target URL
```
Eliminate `--env-vars-file` option if you do not need environment variables or leave the `.env.yaml` empty otherwise you will get an error on deployment.

After a successful deployment of your `skill` on `cloud functions`, you need to share the `Target URL` for your endpoint on cloud functions with the AI Shain team [#pj-ai-shain-support](https://app.slack.com/client/T0256J926/CPXN3K0JE) so that they can configure `HISASHI` to forward the requests to your endpoint.

## 6. Register your skill
Go to [mercari-ai-shain-skills](https://github.com/keito-fukuda/mercari-ai-shain-skills.git) then follow the README.md.

# API Specification
## Request
```
POST / HTTP/1.1
Host: ${Your Skill Endpoint}
```

`payload` should be a string representing valid JSON.

Currently there are 2 types of payload requests supported.

### 1. Slack User Query and Interactive Component Event

`Payload Format`:
| Name             | Type      | Description                                                                 |
|:-----------------|:---------:|:----------------------------------------------------------------------------|
| user             | `Object`  |                                                                             |
|   id             | `String`  | Slack user id (Unique)                                                      |
|   name           | `String`  | Slack user name                                                             |
|   real_name      | `String`  | Slack user real name                                                        |
|   phone          | `String`  | Slack user contact number                                                   |
|   email          | `String`  | Slack user email address                                                    |
| channel          | `Object`  |                                                                             |
|   id             | `String`  | Slack channel id (Unique)                                                   |
|   name           | `String`  | Slack channel name                                                          |
|   type           | `String`  | Slack channel type (private/group/direct_message)                           |
| ts               | `String`  | Slack event timestamp                                                       |
| text             | `String`  | User query in slack                                                         |
| query            | `String`  | User query in slack                                                         |
| intent           | `String`  | Dialogflow detected intent name                                             |
| confidence       | `Number`  | Dialogflow confidence value                                                 |
| lang             | `String`  | Language code for user query                                                |
| params           | `Object`  | Parameters for dialogflow detected intent                                   |
| trigger_id       | `String`  | Trigger id for slack interactive component(button) click event              |
| intent_in_thread | `String`  | Dialogflow detected intent name in slack thread [default  value = `None`]   |
| is_thread        | `Boolean` | User query in slack thread or not [In thread=`True`, Not in thread=`False`] |
| response_url     | `String`  | Slack response url                                                          |

`Sample Payload`:
```
{
   "user": {
       "id": "ABCDEF123",
       "name": "firstname.lastname",
       "real_name": "Full Name",
       "phone": "(143) 333-3333",
       "email": "abcd@email_domain.com",
   },
   "channel": {
       "id": "ABCDEF123",
       "name": "group-ai-shain-req",
       "type": "channel",
   },
   "ts": "1598610482.004000",
   "text": "Input text",
   "query": "Input text",
   "intent": "T_Translation - Text - Yes",
   "confidence": 1.0,
   "lang": "en",
   "params": {
       "param1": "value1",
       "param2": "value2",
       --:--   : --:--
   },
   "trigger_id": "1353122138272.748717076835.7635795da95189a032624b49bec36535",
   "intent_in_thread": "None",
   "is_thread": False,
   "response_url": "https://hooks.slack.com/actions/TABCDEF123/1329488376211/t5AjhGgv6Z8QeBWr7YoDV7zn"
}
```

### 2. Slack Dialog Submission

`Payload Format`:
| Name             | Type      | Description                                                                 |
|:-----------------|:---------:|:----------------------------------------------------------------------------|
| type             | `String`  | Slack event type [type =`dialog_submission`]                                |
| token            | `String`  | Slack app token (Unique)                                                    |
| team             | `Object`  | Slack workspace data                                                        |
|   id             | `String`  | Slack team id                                                               |
|   domain         | `String`  | Slack domain name                                                           |
| user             | `Object`  | Slack user data                                                             |
|   id             | `String`  | Slack user id (Unique)                                                      |
|   name           | `String`  | Slack user name                                                             |
| channel          | `Object`  | Slack channel data                                                          |
|   id             | `String`  | Slack channel id (Unique)                                                   |
|   name           | `String`  | Slack channel name                                                          |
| submission       | `Object`  | Data entered by user in slack dialog                                        |
| callback_id      | `String`  | Callback id set in dialogflow intent response                               |
| user_title       | `String`  | Slack user designation/position/title                                       |
| action_ts        | `String`  | Slack event timestamp                                                       |
| state            | `String`  | Language code for user query                                                |
| response_url     | `String`  | Slack response url                                                          |

`Sample Payload`:
```
{
   "type": "dialog_submission",
   "token": "abcdefghijkl1234",
   "action_ts": "1598611694.461795",
   "team": {
      "id": "TABCDEF123",
      "domain": "abcdefghijkl"
   },
   "user": {
      "id": "ABCDEF123",
      "name": "firstname.lastname",
      "title": "Senior Developer"
   },
   "channel": {
      "id": "ABCDEF123",
      "name": "group-ai-shain-req"
   },
   "submission": {
      "data1": "value1",
      "data2": "value2",
       --:-- : --:--
   },
   "callback_id": "T_Translation_Text_Yes",
   "response_url": "https://hooks.slack.com/app/TABCDEF123/1353152152704/EOajVmIGyjvYPDdkZSDknJCO",
   "state": "en",
}
```

## Response
Response format send to webhook from your skill

`response` should be a string representing valid JSON.

Currently there are 2 types of responses supported.

### 1. Post Slack Message

`Payload Format`:
| Name             | Type      | Description                                                                 |
|:-----------------|:---------:|:----------------------------------------------------------------------------|
| slack            | `Boolean` | Response to slack or not [to slack=`True`,not to slack=`False`]             |
| type             | `String`  | Type of response [Here value is `message`]                                  |
| message          | `String`  | Message to be posted to slack                                               |
| channel          | `String`  | Slack channel id where message to be post                                   |
| thread_ts        | `String`  | Timestamp for slack thread to post message in a thread                      |


`Sample Payload`:
```
{
   "slack": True,
   "type": "message",
   "message": "Please give me a Google Slide or Google Docs URL.",
   "channel": "ABCDEF123",
   "thread_ts": "1598612489.000300"
}
```

### 2. Open Slack Dialog

`Payload Format`:
| Name             | Type      | Description                                                                 |
|:-----------------|:---------:|:----------------------------------------------------------------------------|
| slack            | `Boolean` | Response to slack or not [to slack=`True`,not to slack=`False`]             |
| type             | `String`  | Type of response [Here value is `dialog`]                                   |
| dialog           | `String`  | Dialog component to be opened in slack                                      |
| channel          | `String`  | Slack channel id where dialog to be open                                    |
| trigger_id       | `String`  | Trigger id required to open a dialog in slack                               |


`Sample Payload`:
```
{
   "slack": True,
   "type": "dialog",
   "dialog": {
      "callback_id": "T_Translation_Text_Yes",
      "title": "Text Translation",
      "submit_label": "Translate",
      "state": "en",
      "notify_on_cancel": True,
      "elements": [
         {
            "type": "textarea",
            "label": "Text",
            "name": "text",
            "placeholder": "Text"
         }
      ]
   },
   "trigger_id": "1353150953984.748717076835.05018bed51c9de935d76f2085bb61d2a",
   "channel": "ABCDEF123"
}
```

# Repo Structure
## 1. Dependencies - requirements.txt
Manage required packages with `requirements.txt`. 

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