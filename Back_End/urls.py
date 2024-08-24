from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

api_version = "v1"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    path(f"api/{api_version}/accounts/", include("account.urls")),
    path(f'api/{api_version}/contact/', include("main.urls")),
    path(f"api/{api_version}/owner/", include("owner.urls"))
]
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)