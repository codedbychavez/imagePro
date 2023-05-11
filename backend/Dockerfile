FROM python:3.8
WORKDIR /app
COPY ./requirements.txt /app
RUN apt-get update && apt-get install --no-install-recommends -y python3-opencv libgl1
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
ENV DOCKER_BUILDKIT=0