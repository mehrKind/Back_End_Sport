from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router1 = DefaultRouter()
router1.register("", views.UserInformation, basename="user_information")

router_profile = DefaultRouter()
router_profile.register("", views.UserProfileInformation, basename="user_profile")

allProfileRouter = DefaultRouter()
allProfileRouter.register("", views.UserAllProfileInformation, basename="all_user_profile")

restPassRouter = DefaultRouter()
restPassRouter.register(r'password_recovery', views.PasswordRecoveryViewSet, basename='password_recovery')

changePasswordRouter = DefaultRouter()
changePasswordRouter.register(r'change_password', views.ChangePassword, basename="change_password")

# saveStepRouter = DefaultRouter()
# saveStepRouter.register(r"save_step", views.SaveSteps, basename="save_step")

app_name = "account"
urlpatterns = [
    path("all_users", views.All_user, name="all_users"),
    path("user_info", include(router1.urls), name="user_info"),
    path("user_profile", include(router_profile.urls), name="user_profile_info"),
    path("user_all_profile", include(allProfileRouter.urls)),
    path("register/", views.RegisterUser.as_view(), name="user_register"),
    path("", include(restPassRouter.urls)),
    path("", include(changePasswordRouter.urls)),
    # path("", include(saveStepRouter.urls)),
    path("logout", views.LogoutUser.as_view(), name="user_logout")
]
