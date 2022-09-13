from rest_framework.permissions import (AllowAny)
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model 

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    APIView for account creation (signup)
    """
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer