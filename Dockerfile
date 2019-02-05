FROM python:3.7.1
COPY requirements.txt /way_to_home/requirements.txt
WORKDIR /way_to_home/
RUN pip install -r requirements.txt
