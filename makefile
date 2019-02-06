MANAGE_PATH = way_to_home/manage.py


.PHONY: default help
default: help

help:
	@echo "- \033[4mInstall commands\033[0m:"
	@echo "\trequirements  -  install project requirements"
	@echo "\trabbitMQ      -  install rabbitMQ"
	@echo "\tredis         -  install redis"
	@echo "\tpostgres      -  install postgres"
	@echo "\tlogger        -  create file for logs"
	@echo "\t\033[1minstall       -  run all install commands mentioned above\033[0m"
	@echo "- \033[4mBackend commands\033[0m:"
	@echo "\tdjango        -  run django server"
	@echo "\tcelery        -  run celery beat and worker"
	@echo "\tprepare_data  -  run command to prepare data from EasyWay"
	@echo "\tdaemons       -  run gtfs and notifier daemon in the background"
	@echo "\t\033[1mbackend       -  run all backend commands mentioned above\033[0m"
	@echo "- \033[4mAdditional commands\033[0m:"
	@echo "\tlints         -  run projects lints"
	@echo "\ttest          -  run tests"
	@echo "\tfrontend      -  run watcher"
	@echo "\t\033[1mstart         -  run frontend and backend commands\033[0m"


# Install commands
requirements:
	pip install -r requirements.txt
	npm install

logger:
	sudo touch /var/log/way_to_home.log
	sudo chown -R $USER:$USER /var/log/way_to_home.log

rabbitMQ:
	sudo apt-get install -y erlang
	sudo apt-get install rabbitmq-server
	sudo service rabbitmq-server restart || sudo rabbitmq-server

postgres:
	sudo apt-get install postgresql postgresql-contrib
	sudo -u postgres psql -c "CREATE DATABASE postgres"
	sudo -u postgres psql -c "ALTER USER postgres CREATEDB"

redis:
	sudo apt-get install redis-server
	redis-cli ping

install:
	make requirements
	make rabbitMQ
	make logger
	make redis
	make postgres


# Backend commands
db:
	python $(MANAGE_PATH) migrate

django:
	python $(MANAGE_PATH) runserver

celery:
	(cd way_to_home;\
	gnome-terminal -e "bash -c \"celery -A way_to_home worker -l info; exec bash\"";\
	gnome-terminal -e "bash -c \"celery -A way_to_home beat -l info; exec bash\"")

prepare_data:
	python $(MANAGE_PATH) prepare_data

daemons:
	(cd way_to_home/daemons;\
	nohup python gtfs_daemon.py 11 > /dev/null 2>&1 & \
	nohup python notifier_daemon.py > /dev/null 2>&1 &)

telegram_bot:
	(cd way_to_home/telegram_bot;\
	nohup python bot_handler.py > /dev/null 2>&1 &)

backend:
	make db
	make prepare_data
	make telegram_bot
	make daemons
	make celery
	make django


# Frontend commands
frontend:
	gnome-terminal -e "bash -c \"npm start; exec bash\""


# Additional commands
start:
	make frontend
	make backend

lints:
	(cd way_to_home; pylint --rcfile=.pylintrc *)

test:
	(cd way_to_home;\
	coverage run manage.py test;\
	coverage html)
