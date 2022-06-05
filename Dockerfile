# base images for python 
# alpine => light wright version without any unnecessary cependencies 
FROM python:3.9-alpine3.13
LABEL maintainer =  "Philip" 


# tell the docker don't want to buffer the output 
# the outpyt from python will be printer directly print to the console 
ENV PYTHONUNBUFFERED 1

# Copy the requiement file from local machine to this location 
# the requirement file added into the docker image 
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# copy app directory which contains the Django app 
COPY ./app /app 
# working directory 
WORKDIR /app 
#expose port connect to django server 
EXPOSE 8000

ARG DEV=false 
# run command on the alpine image which using when building our image 
# create a new virtual environment that we're goint to use to store our dependencies 
RUN python -m venv /py && \ 
#upgrade the python package manger inside out virtual environment 
    /py/bin/pip install --upgrade pip && \
# install pg package which we're going to need installed inside our Alpine image 
# in order for pyscpg2 to coonect to pg 
    apk add --update --no-cache postgresql-client && \
# install virtual dependencies package install into temp build deps 
# use for remove the package after in docker file 
    apk add --update --no-cache --virtual .tmp-build-deps \
# the package needed in order to install our PG adapter 
        build-base postgresql-dev musl-dev && \
# install the requirement file 
    /py/bin/pip install -r /tmp/requirements.txt && \
# run the shell command in condition  
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # remove the tmp directory to make sure that theres no any extra depen.
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
# update the environment variable inside the image and we;re updating the path environmrnt variabel 
# do not want to wirte the full path when we run in environemnt 
# whenever we run any pthon coomands it will run automatically from out virtual environment 
ENV PATH="/py/bin:$PATH"

USER django-user
