USERNAME = way_to_home
MANAGE_PATH = way_to_home/manage.py


.PHONY: default usage
default: usage

usage:
	@echo
	@echo 'Usage: make <action>'
	@echo
	@echo '    requirements        setup requirements'
	@echo '    celery worker       run celery worker'
	@echo '    celery beat         run celery beat'
	@echo

requirements:
	pip install -r requirements.txt
	npm install

celery:
	(cd way_to_home;\
	gnome-terminal -e "bash -c \"celery -A way_to_home worker -l info; exec bash\"";\
	gnome-terminal -e "bash -c \"celery -A way_to_home beat -l info; exec bash\"")

#backend:
#	gnome-terminal -e "bash -c \"make celery worker; exec bash\""
#	gnome-terminal -e "bash -c \"cd way_to_home; make celery beat; exec bash\""


#frontend:
#	make install
#	make build

#start:
#	make frontend
#	make backend

#