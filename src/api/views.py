from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from .viewsets.missing import *
from .viewsets.search import *
from .serializers import *
from .utils import get_user
from .models import KnownMissingPerson

import jwt
import datetime

from django.http import JsonResponse


@csrf_exempt
def missing(request):
    view_set = MissingViewSet(request)
    return view_set.respond()


@csrf_exempt
def missing_id(request, pk):
    view_set = MissingIdViewSet(request, pk)
    return view_set.respond()


@csrf_exempt
def find(request):
    view_set = FindMissingViewSet(request)
    return view_set.respond()


@csrf_exempt
def profile(request):
    user = get_user(request)
    reported_cases = KnownMissingPerson.objects.filter(contactPerson=user).all()
    reported_cases = [case.serialize() for case in reported_cases]
    return JsonResponse(reported_cases, safe=False)


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}
        return response


class UserView(APIView):
    def get(self, request):
        user = get_user(request)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response
