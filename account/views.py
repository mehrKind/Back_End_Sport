from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import APIView, api_view, action
from rest_framework import status
from account.serializer import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens  import RefreshToken
from account import models
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView


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

        queryset = User.objects.filter(username=user.username).values("id", "username", "password", "first_name", "last_name",
                                                                      "last_login", "date_joined")

        return queryset


# show the all user information => accounts model

class UserProfileInformation(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = models.UserProfile.objects.filter(user=user).all()
        return queryset
    def get_object(self):
        return self.get_queryset().first()


# show all profile information with user id
class UserAllProfileInformation(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# logout user
class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class RegisterUser(APIView):
# register user class POST method => 201_Createdclass RegisterUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # user models serialize
        UserSerializerData = UserSerializer(data=request.data)
        password = request.data.get("password")
        username = request.data.get("username")
        if UserSerializerData.is_valid():
            user = UserSerializerData.save()
            user.set_password(password)  # Correct way to set password
            user.save()
            # create or update UserProfile
            models.UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phoneNumber': request.data.get('phoneNumber', '')
                }
            )

            refresh = RefreshToken.for_user(user)
            response = {
                "refresh": str(refresh),
                "access" : str(refresh.access_token)
            }

            return Response(response, status.HTTP_201_CREATED)
        else:
            print(UserSerializerData.errors)
            return Response({"error": "user serializer is not valid"}, status.HTTP_400_BAD_REQUEST)



# password recovery

class PasswordRecoveryViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    def create(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        if user:
            random_number = randint(1000, 9999)
            request.session['random_number'] = random_number
            request.session['email'] = email
            subject = "reset password"
            message = "your message"
            from_mail = settings.EMAIL_HOST_USER
            to_list = [email]
            # html content and the style for the code email
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .email-container {{
                        width: 80%;
                        margin: auto;
                        background-color: white;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                    }}
                    .welcome-text {{
                        color: #3498db;
                        font-size: 2rem;
                        margin-bottom: 20px;
                    }}
                    .instruction-text {{
                        font-size: 1.2rem;
                        margin-bottom: 30px;
                    }}
                    .code {{
                        background-color: #333;
                        color: #fff;
                        padding: 10px;
                        border-radius: 20px;
                        font-size: 2rem;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <h1 class="welcome-text">Welcome Back To The Step</h1>
                    <p class="instruction-text">Please enter this code:</p>
                    <h1 class="code">{random_number}</h1>
                </div>
            </body>
            </html>
            """
            send_mail(subject, message, from_mail, to_list, fail_silently=True, html_message=html_content)
            return Response({'detail': 'Code sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        digit_number = request.data.get('digit')
        if 'random_number' in request.session and int(digit_number) == request.session['random_number']:
            return Response({'detail': 'Code is correct'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Code is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(viewsets.ModelViewSet):
    # authentication_classes = []
    permission_classes = [AllowAny]
    def create(self, request):
        # get the password and the confirmation pass
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        email = request.session.get("email")

        # check the password is same as its confirmation
        if not new_password or not confirm_password:
            return Response({"detail": "both password and confirm is required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"detail": "password does not match"})

        # find the user by email => if the user exists then change the password to the new password
        # if the user not exists then return 404 not found status
        user = User.objects.filter(email=email).first()
        if user:
            user.password = make_password(new_password)
            user.save()
            # clear the request session data (sent code and the email address)
            if 'random_number' in request.session:
                del request.session['random_number']
            if 'email' in request.session:
                del request.session['email']
            return Response({"detail": "password changed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class SaveSteps(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return models.UserProfile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
