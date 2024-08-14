# Testing service


## Specification
<details><summary>Expand</summary>

### Summary
A testing service needs to be done. There are test sets with answer options, one or more options must be correct

### Functional parts of the service
* User registration
* User authentication
* Registered users can:
  * Pass any of the test sets
  * Consistently answer all questions, each question must be displayed on a new page with the form submission (re-answering and leaving unchecked is not allowed)
  * After completing the test, you can see the result:
    * number of correct/incorrect answers
    * percentage of correct answers

### Admin panel sections
* Standard user section
* Section with test sets
* Ability to:
  * add questions
  * add answers to questions
  * mark correct answers
* Validation that there must be at least 1 correct option
* Validation that all options cannot be correct
* Deleting questions/answers/changing correct solutions when editing the test sets

### Requirements
* A list of all dependencies should be stored in `requirements.txt`, so you can install them with `pip install -r requirements.txt`
* Development should be done in `.venv`, but the `.venv` directory itself should be added to `.gitignore`
* Settings should be stored in `settings.py`, but also, if there is `settings_local.py` in the same directory, the settings from `settings_local.py` should override the settings in `settings.py`. If there is a `settings_local.py` file, the settings defined in it have higher priority. The `settings_local.py` file itself is added to `.gitignore`. Thus, each developer and beta server can use custom settings
</details>

## Technologies

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-v5.0.7-blue?logo=Django)](https://www.djangoproject.com/)
[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?logo=SQLite)](https://www.sqlite.com/version3.html)
[![docker_compose](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)

## Installation

### Prerequisites
* [Docker](https://www.docker.com/products/docker-desktop/) installed on your system
* Git installed

### Step 1: Clone the repository

1) Open your terminal (Command Prompt, PowerShell, or Git Bash)

2) Navigate to the directory where you want to clone the project:
```
cd /path/to/your/directory
```
or for Windows:
```
cd "C:\Path\To\Your\Directory"
```

3) Clone the repository using Git
```
git clone https://github.com/SZyablov/testing-service.git
```

4) Move into the project directory
```
cd <project-directory-name>
```

### Step 2: Build and run the docker containers

1) Make sure the project contains a `Dockerfile` and `docker-compose.yml` file. These files define how the Docker container will be built and run
2) Build the Docker container using Docker Compose
```
docker-compose build
```
and run it
```
docker-compose up -d
```

Debug test sets will be created automatically. The testing service will run on port 8000

### Step 3: Create superuser

1) View running containers
```
docker-compose ps
```
2) See the SERVICE column in the container row to use it in command to create superuser
```
docker-compose exec -ti <service-name> python3 testing/manage.py createsuperuser
```
3) Follow the prompts to set up the username, email, and password for the project superuser

## Usage

### For user

1) Open http://127.0.0.1:8000/sign-up/ and sign-up
2) You will be redirected to the login page. Login with username and password
3) Choose any test set
4) Answer questions
5) Once you have answered all the questions, you will get a results screen
6) You can logout using the logout link

You can leave questions unanswered and continue the test from where you left off

### For admin

1) Open http://127.0.0.1:8000/admin/ and login with superuser credentials
2) Open "Test sets" table and click "Add test set" (or just press "+ Add")
    1) Enter test set name and description
    2) Press "Save"
    3) You can add questions before saving by pressing "Add another Question" and entering a question in corresponding field
3) Open "Questions" table and click "Add question" (or just press "+ Add")
    1) Choose a test set for the question
    2) Enter text for the question
    3) Add answers and indicate whether they are correct or not by pressing "Add another Answer" and checking the appropriate checkboxes

You can also edit previously created test sets, questions and answers
