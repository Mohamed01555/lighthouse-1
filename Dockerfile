FROM python:3
COPY .  /usr/app
WORKDIR /usr/app
RUN pip install -r requirements.txt
WORKDIR /usr/app/src
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]