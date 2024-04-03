from django.contrib import admin
from . import models

# show the importes modeld into django admin pannel

# showe user profile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "phoneNumber", "weight", "height")
    # search the table with the feilds
    search_fields = ["user__username", "phoneNumber", "city"]
    class Meta:
        model = models.UserProfile
        fields = "__all__"

# show sports place
class UserSportPlaceAdmin(admin.ModelAdmin):
    class Meta:
        model = models.SportPlace
        fields = "__all__"

# show boost user
class BoostUserAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'ModelName'
        model = models.BoostUser
        fields = "__all__"


# register the models
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.SportPlace, UserSportPlaceAdmin)
admin.site.register(models.BoostUser, BoostUserAdmin)

