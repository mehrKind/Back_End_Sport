from django.contrib import admin
from . import models

class DailyAdmin(admin.ModelAdmin):
    list_display = ["user", "completeStep", 'traveledDistance', "kalory", "dayDate", "dailyExercise"]
    search_fields = ["user__username"]
    list_editable = ["completeStep"]
    class Meta:
        model = models.DailyInfo
        fields = "__all__"


admin.site.register(models.DailyInfo, DailyAdmin)