FROM python:3.11

WORKDIR usr/src/polymedic_rest

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/polymedic_rest