FROM python:3.11-slim as backend

WORKDIR /singuletter

COPY ./backend .

RUN pip install -r ./requirements.txt

EXPOSE 4000