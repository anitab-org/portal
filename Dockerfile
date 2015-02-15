FROM python:2.7 
MAINTAINER Ana Balica <ana.balica@gmail.com>
EXPOSE 8000

WORKDIR /usr/src
RUN mkdir portal
RUN cd portal
WORKDIR /usr/src/portal
COPY requirements/prod.txt /usr/src/portal/requirements/prod.txt
RUN pip install -r requirements/prod.txt

