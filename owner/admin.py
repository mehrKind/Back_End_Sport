from django.contrib import admin
from . import models



class DailyAdmin(admin.ModelAdmin):
    list_display = ["user", "totalStep", "completeStep",
                    'score', "calory", "dayDate", "dailyExercise"]
    search_fields = ["user__username", "dayDate", "user__email"]
    list_editable = ["completeStep"]
    list_display_links = ["user"]

    class Meta:
        model = models.DailyInfo
        fields = "__all__"
        


@admin.register(models.ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_textBody', 'send_date',)  # add other fields if needed
    search_fields = ('textBody',)

    def short_textBody(self, obj):
        return f"{obj.textBody[:19]} ..."  # adjust the number as needed

    short_textBody.short_description = 'user_Message'  # this is the column title



admin.site.register(models.DailyInfo, DailyAdmin)
