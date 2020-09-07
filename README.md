# {YOUR_SKILL_NAME}

# Prerequisites
- Python 3.x (You can build your skill in a different language as long as you pick a language supported on cloud functions)
- Cloud Functions on GCP

# Setup
## 1. Clone the repo
```
$ git clone git@github.com:kouzoh/mercari-ai-shain-skills-{YOUR_SKILL_NAME}.git
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
$ gcloud functions deploy --trigger-http --env-vars-file .env.yaml --runtime python37 --allow-unauthenticated --entry-point main {YOUR_SKILL_NAME}
$ gcloud functions describe {YOUR_SKILL_NAME}
```
Remove `--env-vars-file .env.yaml` if you do not need any ENV VARS. 

# Logs
```
$ gcloud functions logs read {YOUR_SKILL_NAME}
```