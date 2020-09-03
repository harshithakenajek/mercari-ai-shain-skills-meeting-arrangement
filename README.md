# Skill Boilerplate
This is a repo which acts as a template for developers to create your own skill endpoint on cloud functions in a much faster and efficient way.

# Prerequisites
- Python 3.x (You can build your skill in a different language as long as you pick a language supported on cloud functions)
- Cloud Functions on GCP

If you would like to build your skill on a different platform, that's fine as long as your skill provides necessary HTTPs endpoint.<br/>
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
Eliminate `--env-vars-file` option if you do not need environment variables or leave the `.env.yaml` empty otherwise you will get an error on deployment.<br/>
<br/>
After a successful deployment of your `skill` on `cloud functions`, you need to share the `Target URL` for your endpoint on cloud functions with the AI Shain team [#pj-ai-shain-support](https://app.slack.com/client/T0256J926/CPXN3K0JE) so that they can configure `HISASHI` to forward the requests to your endpoint.

## 6. Register your skill
Go to [mercari-ai-shain-skills](https://github.com/keito-fukuda/mercari-ai-shain-skills.git) then follow the README.md.

# API Specification

## Request
```
POST / HTTP/1.1
Host: ${Your Skill Endpoint}
```

`Payload` should be a string representing valid JSON.<br/>
Currently there are 2 types of payload requests supported.

### 1. User Query and Interactive Component Event(e.g. Buttons)

`Payload Format`:
| Name               | Type      | Description                                                                 |
|:-------------------|:----------|:----------------------------------------------------------------------------|
| client             | `String`  | `slack`                                                                     |
| type               | `String`  | `message`                                                                   |
| user               | `Object`  |                                                                             |
|   id               | `String`  | Slack user id (Unique)                                                      |
|   name             | `String`  | Slack user name                                                             |
|   real_name        | `String`  | Slack user real name                                                        |
|   phone            | `String`  | Slack user contact number                                                   |
|   email            | `String`  | Slack user email address                                                    |
|   title            | `String`  | Slack user designation/position/title                                       |
| channel            | `Object`  |                                                                             |
|   id               | `String`  | Slack channel id (Unique)                                                   |
|   name             | `String`  | Slack channel name                                                          |
|   type             | `String`  | Slack channel type (private/group/direct_message)                           |
| ts                 | `String`  | Slack event timestamp                                                       |
| data               | `Object`  |                                                                             |
|   text             | `String`  | User query in slack                                                         |
|   query            | `String`  | User query in slack                                                         |
|   intent           | `String`  | Dialogflow detected intent name                                             |
|   confidence       | `Number`  | Dialogflow confidence value                                                 |
|   lang             | `String`  | Language code for user query                                                |
|   params           | `Object`  | Parameters for dialogflow detected intent                                   |
|   trigger_id       | `String`  | Trigger id for slack interactive component(button) click event              |
|   intent_in_thread | `String`  | Dialogflow detected intent name in slack thread [default  value = `None`]   |
|   is_thread        | `Boolean` | User query in slack thread or not [In thread=`True`, Not in thread=`False`] |
|   response_url     | `String`  | Slack response url                                                          |

`Sample Payload`:
```
{
  "client": "slack",
  "type": "message",
  "user": {
    "id": "ABCDEF123",
    "name": "firstname.lastname",
    "real_name": "Full Name",
    "phone": "(143) 333-3333",
    "email": "abcd@email_domain.com",
    "title": "Senior Developer"
  },
  "channel": {
    "id": "ABCDEF123",
    "name": "group-ai-shain-req",
    "type": "channel",
  },
  "ts": "1598610482.004000",
  "data": {
    "text": "Input text",
    "query": "Input text",
    "intent": "T_Translation - Text - Yes",
    "confidence": 1.0,
    "lang": "en",
    "params": {
      "param1": "value1",
      "param2": "value2",
    },
    "trigger_id": "1353122138272.748717076835.7635795da95189a032624b49bec36535",
    "intent_in_thread": "None",
    "is_thread": False,
    "response_url": "https://hooks.slack.com/actions/TABCDEF123/1329488376211/t5AjhGgv6Z8QeBWr7YoDV7zn"
   }
}
```

### 2. Dialog Submission

`Payload Format`:
| Name               | Type      | Description                                                                 |
|:-------------------|:----------|:----------------------------------------------------------------------------|
| client             | `String`  | `slack`                                                                     |
| type               | `String`  | `dialog`                                                                    |
| user               | `Object`  |                                                                             |
|   id               | `String`  | Slack user id (Unique)                                                      |
|   name             | `String`  | Slack user name                                                             |
|   real_name        | `String`  | Slack user real name                                                        |
|   phone            | `String`  | Slack user contact number                                                   |
|   email            | `String`  | Slack user email address                                                    |
|   title            | `String`  | Slack user designation/position/title                                       |
| channel            | `Object`  |                                                                             |
|   id               | `String`  | Slack channel id (Unique)                                                   |
|   name             | `String`  | Slack channel name                                                          |
|   type             | `String`  | Slack channel type (private/group/direct_message)                           |
| ts                 | `String`  | Slack event timestamp                                                       |
| data               | `Object`  |                                                                             |
|   submission       | `Object`  | Data submitted by user in slack dialog                                      |
|   callback_id      | `String`  | Callback id set in dialogflow intent response                               |                                    |
|   action_ts        | `String`  | Slack event timestamp                                                       |
|   state            | `String`  | Language code for user query                                                |
|   response_url     | `String`  | Slack response url                                                          |

`Sample Payload`:
```
{
  "client": "slack",
  "type": "dialog",
  "user": {
    "id": "ABCDEF123",
    "name": "firstname.lastname",
    "real_name": "Full Name",
    "phone": "(143) 333-3333",
    "email": "abcd@email_domain.com",
    "title": "Senior Developer"
  },
  "channel": {
    "id": "ABCDEF123",
    "name": "group-ai-shain-req"
    "type": "channel",
  },
  "ts": "1598610482.004000",
  "data": {
    "submission": {
      "data1": "value1",
      "data2": "value2",
    },
    "callback_id": "T_Translation_Text_Yes",
    "action_ts": "1598611694.461795",
    "state": "en",
    "response_url": "https://hooks.slack.com/app/TABCDEF123/1353152152704/EOajVmIGyjvYPDdkZSDknJCO",
  }
}
```

## Response
Response format sent to webhook from your skill.<br/>
`Payload` should be a string representing valid JSON.<br/>
Currently there are 4 types of responses supported depending on `type`, `data` field has a different structure underneath.

### 1. No Message to Deliver

You can simply return empty json.
```
{}
```

### 2. Deliver Message

`Payload Format`:
| Name             | Type      | Required  | Description                                                     |
|:-----------------|:----------|:----------|:----------------------------------------------------------------|
| client           | `String`  | YES       | `slack`                                                         |
| type             | `String`  | YES       | `mnessage`                                                      |
| channel          | `String`  | YES       | Slack channel id where message to be post                       |
| thread_ts        | `String`  | NO        | Timestamp for slack thread to post message in a thread only if you want to deliver response in thread                     |
| data             | `Object`  | YES       | Message to be posted to slack                                   |
|   text           | `String`  | YES       | Text to be posted to slack                                      |
|   attachments    | `Array`   | YES       | Attachements to be posted to slack: please refer to [Slack Document](https://api.slack.com/legacy/interactive-message-field-guide#field-guide__top-level-message-fields__attachment-fields)                                      |

`Sample Payload`:
```
{
  "client": "slack",
  "type": "message",
  "channel": "ABCDEF123",
  "thread_ts": "1598612489.000300"
  "data": {
    "text": "text",
    "attachments": [{
      "text": 'buttons',
      "callback_id": "buttons",
      "actions": [
      {
        'name': 'button_1',
        'text': 'button_1',
        'type': 'button',
        'value': 'button_1'
      },
      {
        'name': 'button_2',
        'text': 'button_2',
        'type': 'button',
        'value': 'button_2'
      }
      ]
    }]
  }
}
```

### 3. Async Response
Sometime your skill need long time to process and be ready to deliver message back to users.<br/>
In that case, you can imediately return an empty json response, then use `response_url` in request payload to deliver message back to users.<br/>
The `response_url` will be valid up to 5 times within 30 mins.<br/>
Reference: [Slack Document](https://api.slack.com/legacy/interactive-messages#making-messages-interactive__building-workflows__responding-to-message-actions)


### 4. Open Dialog

`Payload Format`:
| Name             | Type      | Required  | Description                                                                 |
|:-----------------|:----------|:----------|:----------------------------------------------------------------------------|
| client           | `String`  | YES       | `slack`                                                                     |
| type             | `String`  | YES       | `dialog`                                                                    |
| channel          | `String`  | YES       | Slack channel id where dialog to be open                                    |
| data             | `Object`  | YES       | Payload for dialog: Please refer to [Slack Document](https://api.slack.com/dialogs#dialogs__opening-a-dialog) |

`Sample Payload`:
```
{
  "slack": True,
  "type": "dialog",
  "channel": "ABCDEF123"
  "data": {
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
  }
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
Multi-lingual support for your service has been performed by including required locale files under `locales` directory.<br/>
For instance,<br/>
Add `ja.yaml` file which includes messages in Japanese<br/>
Add `en.yaml` file which includes messages in English<br/>
As of today, HISASHI supports only `Japanese` & `English`.