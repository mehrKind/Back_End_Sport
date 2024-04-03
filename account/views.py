from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import APIView, api_view, action
from rest_framework import status
from account.serializer import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from account import models
from rest_framework.permissions import AllowAny, IsAdminUser
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from django.core.exceptions import ObjectDoesNotExist


@api_view(["GET"])
def All_user(request: Request):
    if request.method == "GET":
        user_models = User.objects.all()
        serializeUser = UserSerializer(user_models, many=True)
        return Response({"status": 200, "data": f"{serializeUser.data}", "error": "null"}, status.HTTP_200_OK)
    else:
        return Response({"status": 400, "data": "null", "error": "method not allowed"}, status.HTTP_200_OK)


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
        try:
            return self.get_queryset().first()
        except ObjectDoesNotExist as e:
            return Response({"status": 404, "data": "null", "error": str(e)}, status.HTTP_200_OK)


# show all profile information with user id
# todo: NEW UPDATE
class UserAllProfileInformation(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = models.UserProfile.objects.all()
        if not queryset:
            raise ObjectDoesNotExist("No UserProfile objects found.")
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except ObjectDoesNotExist as e:
            return Response({"status": 404, "data": "null", "error": str(e)}, status.HTTP_200_OK)


# logout user
class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# registerUser


class RegisterUser(APIView):
    # register user class POST method => 201_Createdclass RegisterUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # user models serialize
        UserSerializerData = UserSerializer(data=request.data)
        # get the username and password from request
        password = request.data.get("password")
        username = request.data.get("username")
        if UserSerializerData.is_valid():
            user = UserSerializerData.save()
            user.set_password(password)  # set passeord to be hashed
            user.save()
            # create or update UserProfile
            models.UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    # save the phoneNumber in the register page
                    'phoneNumber': request.data.get('phoneNumber', '')
                }
            )

            refresh = RefreshToken.for_user(user)
            response = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)  # access token to login
            }

            return Response(response, status.HTTP_201_CREATED)
        else:
            # print(UserSerializerData.errors)
            return Response({"status": 500, "data": "null", "error": "username is unique"}, status.HTTP_200_OK)


# password recovery
class PasswordRecoveryViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get('email')  # email from  request
        try:

            user = User.objects.filter(email=email)  # find the user by email
            # user = get_object_or_404(User, email=email)
            if user:
                # ? create a random number to send the email
                random_number = randint(1000, 9999)
                # save the email address to the request session
                request.session['random_number'] = random_number
                request.session['email'] = email
                # Email Config and send the 4 digit code
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
                # send mail
                send_mail(subject, message, from_mail, to_list,
                          fail_silently=True, html_message=html_content)
                context = {
                    "status": 200,
                    "data": f"{random_number}",
                    "error": "null"
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    "status": 404,
                    "data": f"user not found",
                    "error": "null"
                }
                return Response(context, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            context = {
                "status": 404,
                "data": f"user not found",
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        # get the 4 digit numbr from request
        digit_number = request.data.get('digit')
        # check if the given code is correct in the form
        if 'random_number' in request.session and int(digit_number) == request.session['random_number']:
            context = {
                'status': 200,
                "data": "code is correct",
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'status': 404,
                "data": "null",
                "error": "Code is incorrect"
            }
            return Response(context, status=status.HTTP_200_OK)


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
            return Response({"status": 400, "data": "null", "error": "both password and confirm is required"}, status.HTTP_200_OK)

        if new_password != confirm_password:
            return Response({"status": 400, "data": "null", "error": "password does not match"}, status.HTTP_200_OK)

        # find the user by email => if the user exists then change the password to the new password
        user = User.objects.filter(email=email).first()
        if user:
            user.password = make_password(new_password)
            user.save()
            # clear the request session data (sent code and the email address)
            if 'random_number' in request.session:
                del request.session['random_number']
            if 'email' in request.session:
                del request.session['email']
            # response request data
            context = {
                "status": 200,
                "data": "password changed successfully",
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            # request respons error
            context = {
                "status": 404,
                "data": "null",
                "error": 'user not found'
            }
            return Response(context, status=status.HTTP_200_OK)


class SaveSteps(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return models.UserProfile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # set partial=True to update a data partially
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "data": serializer.data, "error": "null"})
        context = {
            "status": 400,
            "data": "null",
            "error": f"{serializer.error}"
        }
        return Response(context, status=status.HTTP_200_OK)


# referrer score
# TODO: new update
class referrerScore(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # get the code from request
        referrer_code = request.data.get("referrerCode")
        if not referrer_code:
            return Response({"status": 400, "data": "null", "error": "referrer_code is requierd"}, status.HTTP_200_OK)
        try:
            # find the user who the owner of the code
            userProfile = models.UserProfile.objects.get(
                referrer_code=referrer_code)
            # gift score number to add
            GiftScore = 100
            first_score = userProfile.score
            userProfile.score += GiftScore
            # update the score field and the some of the score and the  giftScore
            userProfile.save(update_fields=['score'])
            data_context = {
                "code": referrer_code,
                "gift_score": GiftScore,
                "first_score": first_score,
                "updated_score": userProfile.score
            }
            return Response({"status": 200, "data": data_context, "error": "null"}, status.HTTP_200_OK)
        # if there was no person to be the owner of the code OR if the code is not exist
        except ObjectDoesNotExist as e:
            return Response({"status": 404, "data": "null", "error": str(e)}, status.HTTP_200_OK)
