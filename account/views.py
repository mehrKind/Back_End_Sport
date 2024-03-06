from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import APIView, permission_classes
from rest_framework import status
from account.serializer import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from account import models


@api_view(["GET"])
def All_user(request: Request):
    if request.method == "GET":
        user_models = User.objects.all()
        serializeUser = UserSerializer(user_models, many=True)
        return Response(serializeUser.data, status.HTTP_200_OK)
    else:
        return Response(None, status.HTTP_400_BAD_REQUEST)


# show the user information => django User model
class UserInformation(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # get the current user
        user = self.request.user

        queryset = User.objects.filter(username=user.username).values("username", "password", "first_name", "last_name",
                                                                      "last_login", "date_joined")

        return queryset


# show the all user information => accounts model
class UserProfileInformation(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = models.UserProfile.objects.filter(user=user).all()

        return queryset


class LogoutUser(APIView):
    def get(self):
        self.request.user.auth_token.delete()
        return Response({'detail':'user successfully logout'}, status.HTTP_200_OK)
