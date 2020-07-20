FROM ubuntu:latest

RUN apt-get update && \
        apt-get install -y software-properties-common && \
        add-apt-repository ppa:deadsnakes/ppa && \
        apt-get update -y && \
        apt-get install -y build-essential python3.6 python3.6-dev python3-pip && \
        apt-get install -y git  && \
        # update pip
        python3.6 -m pip install pip --upgrade && \
        python3.6 -m pip install wheel
#FROM python:3.8.0-alpine
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev linux-headers libc-dev
#RUN apk update && apk upgrade && apk add gcc musl-dev libc-dev libc6-compat linux-headers build-base git libffi-dev openssl-dev postgresql-dev

COPY . /app
WORKDIR /app
ARG  APP_SETTINGS="expenses.config.DevelopmentConfig"
ARG  DB_PASS_DEV="password"
ARG  DATABASE_URL="postgres://wojhkgcclswuni:22fd79c72b5bf99e8262936f655729d5a33fcd74c6ce7c59c4ed7be3597847a1@ec2-107-20-176-7.compute-1.amazonaws.com:5432/dfc93l56vn7kv6"
ARG  EMAIL_USERNAME="expenseprofessional@gmail.com"
ARG  EMAIL_PASSWORD="wbxsscvrkfmcswxm"

RUN pip install -r requirements.txt
#ENTRYPOINT ["python3"]
ENTRYPOINT ["python3"]
CMD ["create_db.py"]