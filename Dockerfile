# BACKEND - Image
FROM python:3.11-slim as backend
WORKDIR /singuletter
COPY ./backend .
RUN pip install -r ./requirements.txt
EXPOSE 4000

# API - Image
FROM python:3.11-slim as ai_app
WORKDIR /ai_app
COPY ./api /ai_app
RUN pip install -r /ai_app/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/ai_app"
EXPOSE 8001
