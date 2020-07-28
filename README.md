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
$ gcloud functions deploy ${FUNCTION_NAME} --trigger-http --env-vars-file .env.yaml --runtime python37 --entry-point main
$ gcloud functions describe ${FUNCTION_NAME} // Get a Target URL
```
*Eliminate `--env-vars-file` option if you do not need environment variables or leave the `.env.yaml` empty otherwise you will get an error on deployment.

After a successful deployment of your `skill` on `cloud functions`, you need to share the `Target URL` for your endpoint on cloud functions with the AI Shain team(#pj-ai-shain-support) so that they can configure `HISASHI` to forward the requests to your endpoint.

# Logs
```
$ gcloud functions logs read ${FUNCTION_NAME}
```