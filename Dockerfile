FROM python:3
COPY .  /usr/app
WORKDIR /usr/app/src
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]