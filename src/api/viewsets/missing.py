from .. import models
from django.http import JsonResponse
from django.db import IntegrityError


class MissingViewSet:
    def __init__(self, request):
        self.request = request
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

    def respond(self):
        method = self.verbs[self.request.method]
        response = method()
        return response
