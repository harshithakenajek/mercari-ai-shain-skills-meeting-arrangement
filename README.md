# Meeting Room
With this skill, users can do the following tasks.

1: Meeting Room Availability
Users can check availabile meeting rooms on a specified floor.

2: Meeting Room Booking
Users can find and book a meeting room that meets their needs(duration, room size, floor).

3: Meeting Room Location
Users can know pinpoint location of the specified meeting room on the map.

# Prerequisites
- Python 3.x (You can build your skill in a different language as long as you pick a language supported on cloud functions)
- Cloud Functions on GCP

# Setup
## 1. Clone the repo
```
$ git clone git@github.com:kouzoh/mercari-ai-shain-skills-meetingroom.git
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