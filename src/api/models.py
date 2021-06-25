from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class KnownMissingPerson(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="knownMissingPersonsImages")
    contactPerson = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="knownMissingPersonsContact",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image.url,
        }


class KnownMissingPersonImages(models.Model):
    missingPerson = models.ForeignKey(
        KnownMissingPerson,
        on_delete=models.CASCADE,
        related_name="knownMissingPersonsImages",
    )
    imgPath = models.ImageField(upload_to="knownMissingPersonsImages")

    def __str__(self):
        return f"image for {self.missingPerson}"

    def serialize(self):
        return {"id": self.id, "url": self.imgPath.url}


class UserSeeKnownMissingPerson(models.Model):
    missingPerson = models.ForeignKey(
        KnownMissingPerson,
        on_delete=models.CASCADE,
        related_name="foundKnownMissingPersonsImages",
    )
    imgPath = models.ImageField(upload_to="unknownMissingPersonsImages")
    imgEmbedding = models.JSONField(blank=True, null=True)
    takenBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="knownMissingPersonsImagesTaker",
        default=0,
    )

    def __str__(self):
        return f"image for {self.missingPerson} taken by {self.takenBy}"


class UnKnownMissingPerson(models.Model):
    pass


class UserSeeUnknownMissingPerson(models.Model):
    missingPerson = models.ForeignKey(
        UnKnownMissingPerson,
        on_delete=models.CASCADE,
        related_name="foundUnknownMissingPersonsImages",
    )
    imgPath = models.ImageField(upload_to="unknownMissingPersonsImages")
    imgEmbedding = models.JSONField(blank=True, null=True)
    takenBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="unknownMissingPersonsImagesTaker",
        default=0,
    )

    def __str__(self):
        return f"image for Unknown Missing person taken by {self.takenBy}"
