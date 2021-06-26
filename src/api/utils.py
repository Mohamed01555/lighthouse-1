import jwt
from rest_framework.exceptions import AuthenticationFailed
from .models import User


def get_user(request):
    token = request.COOKIES.get("jwt")

    if not token:
        raise AuthenticationFailed("Unauthenticated!")

    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated!")

    user_id = payload["id"]
    user = User.objects.filter(id=user_id).first()

    return user
