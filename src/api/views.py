from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContactPerson, MissingPerson
from .serializers import ContactPersonSerializer, MissingPersonSerializer
from .classifier.classifier import ImageClassifier

class MissingPersonViewSet(viewsets.ViewSet):
    def show(self, request):
        missing = MissingPerson.objects.all()
        serializer = MissingPersonSerializer(missing, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MissingPersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        missing_person = MissingPerson.objects.get(id=pk)
        serializer = MissingPersonSerializer(missing_person)
        return Response(serializer.data)

    def update(self, request, pk=None):
        missing_person = MissingPerson.objects.get(id=pk)
        serializer = MissingPersonSerializer(instance=missing_person, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        missing_person = MissingPerson.objects.get(id=pk)
        missing_person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchView(APIView):
    def post(self,request):
        classifier = ImageClassifier()
        result = classifier.find(request.data['image'])
        response = None
        if not result:
            result= {"result":"not found"}
            response = Response(result, status=status.HTTP_204_NO_CONTENT)
        return response