from django.contrib import admin
from .models import UserProfile

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile
        fields = "__all__"


admin.site.register(UserProfile, UserProfileAdmin)
