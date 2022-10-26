FROM python:3.10-slim AS init
ENV PATH=/home/application/.local/bin:$PATH

RUN useradd application --home-dir /home/application --uid 1000 \
 && mkdir -p /home/application \
 && chown application:application /home/application

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip


FROM init AS build

# For orjson
COPY --from=rust:1-slim /usr/local/cargo/bin/rustup /usr/loca/bin/rustup

USER application

COPY requirements.txt /home/application/requirements.txt
RUN pip install --user --no-cache-dir -r /home/application/requirements.txt


FROM init AS prod
WORKDIR /app
USER application

COPY --from=build /home/application/.local /home/application/.local
COPY ./app/ /app/

CMD python main.py


FROM init AS dev
ENV DEBUG=True
WORKDIR /app
USER application

COPY --from=build /home/application/.local /home/application/.local

COPY ./requirements_dev.txt /home/application/requirements_dev.txt
RUN pip install --user --no-cache-dir \
      -r /home/application/requirements_dev.txt

CMD python main.py
