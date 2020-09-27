###########
# BUILDER #
###########

# pull  official base image
FROM python:3.7 as builder

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update OS
RUN apt-get update && apt-get install -y netcat

# lint
RUN pip3 install --upgrade pip
RUN pip3 install flake8
COPY . /usr/src/backend/

# install dependencies
COPY ./requirements.txt .
RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/backend/wheels -r requirements.txt


#########
# FINAL #
#########
# pull official base image
FROM python:3.7

# create directory for the app user
RUN mkdir -p /home/backend

# create the app user
RUN groupadd -r backend && useradd -r -g backend backend

# create the appropriate directories
ENV HOME=/home/backend
ENV APP_HOME=/home/backend/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME


# install dependencies
RUN apt-get update && apt-get install -y libpq-dev && apt-get install -y netcat
COPY --from=builder /usr/src/backend/wheels /wheels
COPY --from=builder /usr/src/backend/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R backend:backend $APP_HOME
RUN chown -R backend:backend $HOME/.cache

# change to the app user
USER backend

# run entrypoint.prod.sh # TODO
ENTRYPOINT ["/home/backend/web/entrypoint.prod.sh"]
CMD ["run"]
