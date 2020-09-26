FROM python:3.8.2

WORKDIR /usr/src/fetcher

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

#CMD["run"]