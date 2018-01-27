# Description


backend api restfull Pitchmyjob.

Technology stack :
- Django / django-rest-framework
- AWS : SQS, DynamoDB, RDS, Lambda, ElasticSearch, ElasticBeanstalk




## Installation

### Clone `barneystinson` project

```
cd <path/to/clone/project>
git clone xxxxxxxxx
```

### Install Python 3

```
sudo apt-get install python3 # Ubuntu / Debian
brew install python3 # OS X
```

### Install virtualenvwrapper

```
pip3 install virtualenvwrapper
```

Edit your `.profile` :

```
nano ~/.profile
```

Paste the content bellow :

```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3.6 # Change the path to match your installation
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv # Change the path to match your installation
source /usr/local/bin/virtualenvwrapper.sh # Change the path to match your installation
```

Execute profile

```
source ~/.profile
```

## Create `barneystinson` virtualenv

```
mkvirtualenv barneystinson --no-site-packages
```

## Edit the `postactivate`

```
nano ~/.virtualenvs/barneystinson/bin/postactivate
```

Paste the content bellow :

```
!/bin/zsh (ou #!/bin/bash)

PROJECT_PATH="~/Developpement/barneystinson/barneystinson" # Change it to match your installation

# USEFUL SHORTCUTS
alias cdproject="cd $PROJECT_PATH"
alias run_local="python $PROJECT_PATH/manage.py runserver 0.0.0.0:8000 --settings=settings.local"
alias makemigrations="python $PROJECT_PATH/manage.py makemigrations --settings=settings.local"
alias migrate="python $PROJECT_PATH/manage.py migrate --settings=settings.local"
alias init_data="python $PROJECT_PATH/manage.py init_data --settings=settings.local"
alias reset_db="python $PROJECT_PATH/manage.py reset_db --settings=settings.local"
alias shell="python $PROJECT_PATH/manage.py shell_plus --settings=settings.local"
alias run_flake8="flake8 $PROJECT_PATH"
alias test="python $PROJECT_PATH/manage.py test --settings=settings.local"

# DJANGO SETTINGS
export DJANGO_SETTINGS_MODULE='settings.production'
export DJANGO_SECRET_KEY='<change_me>'
export DJANGO_DB_DEV_HOST='<change_me>'
export DJANGO_DB_DEV_PORT='5432'
export DJANGO_DB_DEV_NAME='<change_me>'
export DJANGO_DB_DEV_USER='<change_me>'
export DJANGO_DB_DEV_PASSWORD='<change_me>'
export DJANGO_DB_PROD_HOST='<change_me>'
export DJANGO_DB_PROD_PORT='<change_me>'
export DJANGO_DB_PROD_NAME='<change_me>'
export DJANGO_DB_PROD_USER='<change_me>'
export DJANGO_DB_PROD_PASSWORD='<change_me>'

# AWS ACCESS
export AWS_ACCESS_KEY_ID='<change_me>'
export AWS_SECRET_ACCESS_KEY='<change_me>'

cdproject
```

Deactivate and reactivate your virtualenv :

```
deactivate && workon barneystinson
```

### Install all dependencies

```
cdproject && pip install -r requirements/local.txt && pip install -r requirements/test.txt
```

### Run project

```
run-local
```

## Shortcuts & commands

* `cdproject` : change the shell working directory to project directory.
* `run_local` : starts the django development Web server
* `makemigrations` : creates new migrations based on the changes detected on models
* `migrate` : synchronizes the database state with migrations
* `init_data` : adds some basics data to the database (Industry, Employee, ContractType, Experience, StudyLevel, Group, User (admins))
* `reset_db` : deletes the current development DBInstance and create a new one
* `shell` : starts the Python interactive interpreter with shell_plus (autoload models)
* `run_flake8` : runs `flake8` to test PEP conventions
* `test` : runs all the tests
