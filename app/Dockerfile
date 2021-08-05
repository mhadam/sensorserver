FROM bynect/hypercorn-fastapi:python3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
&& apt-get -y install python3-dev libpq-dev build-essential \
&& apt-get clean

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt \
--no-cache-dir --no-color --no-python-version-warning --disable-pip-version-check

ENV APP_MODULE="app.api.server:app"

#FROM python:3.8-slim-buster
#
#WORKDIR /backend
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONBUFFERED 1
#
## install system dependencies
#RUN apt-get update \
#  && apt-get -y install netcat gcc postgresql \
#  && apt-get clean
#
## install python dependencies
#RUN pip install --upgrade pip
#COPY ./requirements.txt /backend/requirements.txt
#RUN pip install -r requirements.txt
#
#COPY . /backend

