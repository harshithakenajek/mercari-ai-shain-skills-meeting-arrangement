# Skill Template
This is a template repo which acts as a framework for developers to create their new skill service endpoints(cloud functions in GCP) in a much faster and efficient way


# Setup
## 1 Clone the repo
```
$ git clone git@github.com:keito-fukuda/mercari-ai-shain-skills.git
```
## 2 Rename the repo 
Rename the repo to your skill set name. Please follow the below naming convention for your skill service repo
```
mercari-ai-shain-skills-[SKILL_NAME]
```
## 3 Creating Virtual Environment
This webhook will be run only in `Python 3.6` version. Inorder to manage the version of Python used, we have to create a virtual environment supports `Python 3.6`
```
$ python -m virtualenv -p /usr/bin/python3.6 venv
```
If you are already running Python 3.6, then use below command to create `venv`
```
$ python -m virtualenv venv 
```


# Template Project Structure
## 1. Dependencies - requirements.txt
Manage required packages with requirements.txt. 
If you want to install the dependencies in a virtual environment, create and activate that environment first, then use the Install from requirements.txt command.
```
$ source venv/bin/activate  // actiavte virtual environment
$ pip install -r requirements.txt  // Install all dependencies
```
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
For eg.
Add `ja.yaml` file which includes messages in Japanese
Add `en.yaml` file which includes messages in English


# Deployment
```
$ gcloud config set project ${GCP_PROJECT_NAME}
$ gcloud functions deploy --trigger-http --env-vars-file .env.yaml --runtime=python37 [FUNCTION_NAME]
```

