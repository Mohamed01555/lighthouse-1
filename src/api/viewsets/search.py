from django.http import JsonResponse

from .base import BaseViewSet
from ..classifier.classifier import ImageClassifierSimulator
from ..models import KnownMissingPersonImages


class FindMissingViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.request = request
        self.verbs = {"POST": self.post}

    def post(self):
        target_image = self.request.FILES["image"]
        source_images_qs = KnownMissingPersonImages.objects.all()
        source_images = {image.id: image.imgPath for image in source_images_qs}
        result = ImageClassifierSimulator().find(target_image, source_images)
        try:
            missing_person = KnownMissingPersonImages.objects.get(
                id=result["pk"]
            ).missingPerson
            return JsonResponse(missing_person.serialize(), status=200)
        except KnownMissingPersonImages.DoesNotExist:
            return JsonResponse({"message": "not found"}, status=204)
