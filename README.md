# Way To Home
[![Build Status](https://travis-ci.org/Lv-365python/wayToHome.svg?branch=develop)](https://travis-ci.org/Lv-365python/wayToHome)
[![Coverage Status](https://coveralls.io/repos/github/Lv-365python/wayToHome/badge.svg?branch=develop)](https://coveralls.io/github/Lv-365python/wayToHome?branch=develop)

## Description
WayToHome is a web application for comfortable route tracking which allows setting up of
notifications to get information about transport you want at desired time. The key features
of the system are as follows:
- User can get optimal way from point A to point B.
- User can get an account which allows him to set up notifications.
- User has profile which contains google account photo, information about this user,
his places, ways and active notifications;
- User can create places, ways and notifications;
- User can get notifications when he should go out to get on the transport;
## Technologies
- python - 3.7.1
- django - 2.1.4
- celery - 4.2.1
- redis - 3.0.6
- postgresql - 9.5.14
- nodejs - 10.15.0
- npm - 6.4.1
- reactjs - 16.6.3

## Installing
#### PostgreSQL
```
# install
$ sudo apt-get install postgresql postgresql-contrib

# create user and database
$ sudo -i -u postgres
postgres=# CREATE USER <db_user> PASSWORD '<db_password>'";
postgres=# CREATE DATABASE <db_name> OWNER <db_user>;
postgres=# ALTER USER <db_user> CREATEDB;
```
#### Redis
```
# install
$ sudo apt-get install redis-server

# check connect with redis
$ redis-cli ping
PONG
```
#### RabbitMQ
```
# install
$ sudo apt-get install -y erlang
$ sudo apt-get install rabbitmq-server

# enable and start
$ systemctl enable rabbitmq-server
$ systemctl start rabbitmq-server

# check status
$ systemctl status rabbitmq-server
```
## Project configuration
1. Clone this repository.
2. Create a new folder `easy_way_data` in the project root directory.
3. Activate virtual environment.
#### Backend
1. Go to the folder `requirements.txt` and run command to install required dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Create `localsettings.py` in `way_to_home/way_to_home/` with following settings:
    ```python
    # Database settings
    DATABASES = {
        'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'HOST': 'localhost',
           'USER': '<db_user>',
           'PASSWORD': '<db_password>',
           'NAME': '<db_name>',
        }
    }
    # Nexmo settings
    NEXMO_API_KEY = '<nexmo_api_key>'
    NEXMO_API_SECRET = '<nexmo_api_secret>'
    
    # SMTP settings
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = '<email_host_user>'
    EMAIL_HOST_PASSWORD = '<email_host_password>'
    EMAIL_PORT = 587
    DEFAULT_FROM_EMAIL = '<default_from_email>'
    
    # JWT settings
    JWT_KEY = '<jwt_key>'
    JWT_ALGORITHM = 'HS384'
 
    # Celery settings
    CELERY_BROKER_URL = '<celery_broker_url>'
    
    # Telegram bot settings
    TELEGRAM_BOT_TOKEN = '<telegram_bot_token>'
 
    # Google settings
    CLIENT_ID = '<client_id>'
    CLIENT_SECRET = '<client_secret>'
    GOOGLE_API_KEY = '<google_api_key>'
    ```
3. Go to the folder with `manage.py` file and run migrate: 
    ```
    python manage.py migrate
    ```

#### Frontend
1. Go to the folder with `package.json` and run command:
    ```
    npm install
    ```
2. Create `settings.js` in `way_to_home/static/src` with following settings:
    ```js
    // Required keys for Here App API
    export const HERE_APP_ID = '<here_app_api_id>';
    export const HERE_APP_CODE = '<here_app_api_code>';
    export const GOOGLE_MAP_API = '<google_map_api_key>'
    ```
## Running
1. Go to the project root folder and run watcher: 
    ```
    npm start
    ```
2. Go to the folder `daemons` and run daemon:
    ```
    # daemon for preparing gtfs data from EasyWay
    python gtfs_daemon.py 11
        
    # daemon for assigning celery tasks to prepare notifications
    python notifier_deamon.py
    ```
    
3. Create file `way_to_home.log` in `/var/log/` directory, and add user permissions to that file.
    ```
    sudo touch /var/log/way_to_home.log
    sudo chown -R $USER:$USER /var/log/way_to_home.log
    ```
    
4. Go to the folder with `manage.py` file and run django server: 
    ```
    python manage.py runserver
    ```

5. Go to the django root folder run celery worker and beat: 
    ```
    celery -A way_to_home worker -l info
    celery -A way_to_home beat -l info
    ```
## Addition commands

#### Docker
- To start up your Docker container
    ```
    docker-compose up -d --build
    ```
- To close down your Docker container
    ```
    docker-compose down
    ```

#### Makefile
- To use `makefile` run command in the project root folder:
	```
	makefile help
	```

#### Frontend
- To start react server:
    ```
    npm startserver
    ```
- To build bundle.js:
    ```
    npm build
    ```
- To run watcher:
    ```
    npm start
    ```
    
#### Backend
- To monitor redis changes:
    ```
    redis-cli monitor
    ```
- To purge messages from task queues run in django root folder:
    ```
    celery -A way_to_home purge
    ```


## Developers info
- #### Lv-365.Python:
    - @PetrushynskyiOleksii
    - @meelros
    - @BoroviyOrest
    - @Kardan1123
    - @Sasha1152
    - @dimigor
    - @mizin4ik
    - @vo333ua
