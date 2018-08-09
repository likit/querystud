FROM python:3.6.5

RUN mkdir /querystud
COPY requirements.txt /querystud
WORKDIR /querystud
RUN pip install -r requirements.txt
