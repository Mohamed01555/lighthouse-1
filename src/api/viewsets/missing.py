from .. import models
from django.http import JsonResponse
from django.db import IntegrityError
from .base import BaseViewSet


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
            person = models.KnownMissingPerson(name=name, image=image)
            person.save()
            return JsonResponse(person.serialize(), status=201)
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
        self.verbs = {"GET": self.get, "DELETE": self.delete, "PATCH": self.patch}

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

    def patch(self):
        person = models.KnownMissingPerson.objects.get(id=self.pk)
        data = dict(self.request.PATCH)
        image = self.request.FILES["image"]
        data["image"] = image
        print(data)
        for attribute, value in data.items():
            if isinstance(value, list):
                value = value[0]
            setattr(person, attribute, value)
        person.save()
        return JsonResponse(person.serialize(), status=202)
