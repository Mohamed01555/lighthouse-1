from django.db import models
from django.contrib.auth.models import User


class KnownMissingPerson(models.Model):
    name = models.CharField(max_length=50)
    contactPerson = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="missingPersons"
    )

    def __str__(self):
        return self.name


class KnownMissingPersonImages(models.Model):
    missingPerson = models.ForeignKey(
        KnownMissingPerson, on_delete=models.CASCADE, related_name="photos"
    )
    imgPath = models.ImageField(upload_to="knownMissingPersonsImages")
    imgEmbedding = models.JSONField()

    def __str__(self):
        return f"image for {self.missingPerson} taken by {self.takenBy}"


class UserSeeknownMissingPerson(models.Model):
    missingPerson = models.ForeignKey(
        KnownMissingPerson, on_delete=models.CASCADE, related_name="photos"
    )
    imgPath = models.ImageField(upload_to="unknownMissingPersonsImages")
    imgEmbedding = models.JSONField()
    takenBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="takenPhotos", default=0
    )

    def __str__(self):
        return f"image for {self.missingPerson} taken by {self.takenBy}"


class UnKnownMissingPerson(models.Model):
    pass


class UserSeeUnknownMissingPerson(models.Model):
    missingPerson = models.ForeignKey(
        UnKnownMissingPerson, on_delete=models.CASCADE, related_name="photos"
    )
    imgPath = models.ImageField(upload_to="unknownMissingPersonsImages")
    imgEmbedding = models.JSONField()
    takenBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="takenPhotos", default=0
    )

    def __str__(self):
        return f"image for Unknown Missing person taken by {self.takenBy}"
