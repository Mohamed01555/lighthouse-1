from .. import models
from django.http import JsonResponse
from django.db import IntegrityError
from .base import BaseViewSet
import json


class MissingViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.verbs = {"GET": self.get, "POST": self.post}

    def post(self):
        files = self.request.FILES
        data = self.request.POST
        name = data["name"]
        image = files["image"]
        try:
            person = models.KnownMissingPerson(name=name)
            person.save()
            image = models.KnownMissingPersonImages(missingPerson=person, imgPath=image)
            image.save()
            return JsonResponse({"message": "posted"}, status=201)
        except IntegrityError:
            return JsonResponse({"message": "Database integrity error"}, status=500)

    @staticmethod
    def get():
        people = models.KnownMissingPerson.objects.all()
        response = [person.serialize() for person in people]
        return JsonResponse(response, safe=False)


class MissingIdViewSet(BaseViewSet):
    def __init__(self, request, pk):
        super().__init__(request)
        self.pk = pk
        self.verbs = {"GET": self.get, "DELETE": self.delete, "PUT": self.put}

    def get(self):
        try:
            person = models.KnownMissingPerson.objects.get(id=self.pk)
            person = person.serialize()
            return JsonResponse(person, safe=False)
        except IntegrityError:
            return JsonResponse({"message": "Database integrity error"}, status=500)

    def delete(self):
        person = models.KnownMissingPerson.objects.get(id=self.pk)
        person.delete()
        return JsonResponse({"message": "deleted"}, status=204)

    def put(self):
        person = models.KnownMissingPerson.objects.get(id=self.pk)
        data = json.loads(self.request.body)
        for attribute, value in data.items():
            setattr(person, attribute, value)
        person.save()
        return JsonResponse({"message": "edited"}, status=202)
