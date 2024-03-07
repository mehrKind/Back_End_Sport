from django.contrib import admin
from .models import UserProfile, UserHealth, SportPlace

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserHealthAdmin(admin.ModelAdmin):
    class Meta:
        model = UserHealth
        fields = "__all__"


class UserSportPlaceAdmin(admin.ModelAdmin):
    class Meta:
        model = SportPlace
        fields = "__all__"


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserHealth, UserHealthAdmin)
admin.site.register(SportPlace, UserSportPlaceAdmin)

