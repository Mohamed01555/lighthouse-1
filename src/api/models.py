from django.db import models

class MissingPerson(models.Model):
    name = models.CharField(max_length=20)

class ContactPerson(models.Model):
    pass
