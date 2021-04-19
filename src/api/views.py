from .models import KnownMissingPerson, KnownMissingPersonImages
from .classifier.classifier import ImageClassifier
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def missing(request):
    if request.method == "POST":
        files = request.FILES
        data = request.POST
        name = data["name"]
        image = files["image"]
        try:
            person = KnownMissingPerson(name=name)
            person.save()
            image = KnownMissingPersonImages(missingPerson=person, imgPath=image)
            image.save()
            return JsonResponse({"message": "posted"}, status=201)
        except IntegrityError:
            return JsonResponse({"message": "Database integrity error"}, status=500)
    elif request.method == "GET":
        people = KnownMissingPerson.objects.all()
        response = [person.serialize() for person in people]
        return JsonResponse(response, safe=False)
