from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

api_version = "v1"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    path(f"api/{api_version}/accounts/", include("account.urls")),
    # path(f'api/{api_version}/accounts/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # token
    path(f'api/{api_version}/contact/', include("main.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)