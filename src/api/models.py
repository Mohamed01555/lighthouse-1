from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, email, name, password=None, is_admin=False, is_staff=False, is_active=True
    ):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.name = name
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        user = self.create_user(email, name, password, is_admin=True, is_staff=True)
        return user


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]
    objects = UserManager()


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
