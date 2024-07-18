from django.contrib import admin
from . import models


class DailyAdmin(admin.ModelAdmin):
    list_display = ["user", "totalStep", "completeStep",
                    'score', "calory", "dayDate", "dailyExercise"]
    search_fields = ["user__username", "dayDate", "user__email"]
    list_editable = ["completeStep"]
    list_display_links = ["user", "dayDate"]

    class Meta:
        model = models.DailyInfo
        fields = "__all__"


admin.site.register(models.DailyInfo, DailyAdmin)
