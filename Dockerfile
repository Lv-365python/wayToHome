FROM python:3.7.1
RUN mkdir way_to_home
ADD requirements.txt /way_to_home
WORKDIR way_to_home/
RUN pip install -r requirements.txt
ADD . /way_to_home
