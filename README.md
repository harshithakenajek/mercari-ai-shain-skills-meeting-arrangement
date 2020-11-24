# Meeting Room

With this skill, users can do the following tasks.

Meeting arrangement in the specified room, people and duration

# Prerequisites

- Python 3.x (You can build your skill in a different language as long as you pick a language supported on cloud functions)
- Cloud Functions on GCP

# Setup

## 1. Clone the repo

```
$ git clone https://github.com/harshithakenajek/mercari-ai-shain-skills-meeting-arrangement.git
```

## 2. Creating Virtual Environment

```
$ python3 -m venv venv
$ . venv/bin/activate
```

## 3. Installing Packages

```
$ pip install -r requirements.txt
```

## 4. Configuration

```
$ cp .env.template.yaml .env.yaml
```

Then fill each attirbutes for your environment.

## 5. Deplpyment

```
$ gcloud config set project ${GCP_PROJECT_NAME}
$ gcloud functions deploy --trigger-http --env-vars-file .env.yaml --runtime python37 --allow-unauthenticated --entry-point main ${FUNCTION_NAME_FOR_YOUR_SKILL}
$ gcloud functions describe ${FUNCTION_NAME_FOR_YOUR_SKILL}
```

# Logs

```
$ gcloud functions logs read ${FUNCTION_NAME_FOR_YOUR_SKILL}
```
