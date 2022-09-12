# todev

## Summary
todev is a todo app with custom permission clas defind for developers and project manager. They can collaborate with each other on different projects. Each authenticated user can create a project from scratch and become the project manager, add/remove members to/from the project.

## How to run
Simply via Docker:
```
git clone https://github.com/alimghmi/todev.git
cd todev
docke-compose -f docker-compose.dev.yaml up --build
```
Or Set it up manually:
```
git clone https://github.com/alimghmi/todev.git
cd todev/todev
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
### Notes: 
 - docker-compose takes care of env files automatically. Consider adding **env variables** for a better experience, in case of manual setup.
 - Please consider adding a *superuser* via django-admin command line or create a non-super user via `signup` endpoint. 

## Authorization
Todev leverages simple-jwt. All functional endpoints of app (except login/signup) expect you to send a access token as Authorization in the header.

## Browsable API
It's possible to test and examine the app within browser, which is provided by DRF UI. In addition following is possible to be managed via a third party app like curl by providing the brearer token as Authorization key in the request header.


## Endpoints
For further information please check **postman collection** of project, all necessarry fields of each endpoints are documented in details. Postman collection is available [here](https://github.com/alimghmi/todev/blob/master/todev/todev.postman_collection.json). 

User-related operations:
```
POST /signup/: Create a new user

POST /api/token/: Return access/refresh tokens to login
```

Project endpoints:
```
GET /projects/: Return list of projects for user which user is a project manager or a developer of

POST /projets/: Create a new projet by providing the needed fields

PUT /projects/<project_id_here>/: Update a project

GET /projects/<project_id_here>/: Get a detailed view of a project

DELETE /projects/<project_id_here>/: Delete a project
```
Task endpoints:
```
GET projects/<project_id_here>/tasks/: Get all of the tasks in a project

GET projects/<project_id_here>/tasks/?user=me: Get all of current logged in user in a project

GET projects/<project_id_here>/tasks/?user=john: Get all of the tasks of john in a porject

POST /tasks/: Add a new tasks to a project

PUT /tasks/<task_id_here>/: Update a task

DELETE /tasks/<task_id_here>/: Delete a task

```


