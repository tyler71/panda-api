FROM python:3.10-slim as build

RUN useradd application --home-dir /home/application --uid 1000 \
 && mkdir -p /home/application \
 && chown application:application /home/application

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt /home/application/requirements.txt
RUN pip install --no-cache-dir -r /home/application/requirements.txt \
 && rm /home/application/requirements.txt

USER application


COPY ./app/ /app/
WORKDIR /app

CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload


FROM build as prod

CMD uvicorn main:app --host 0.0.0.0 --port 8000
