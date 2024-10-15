from django.contrib import admin
from step import models

# class StepSupportAdmin(admin.ModelAdmin):
#     list_display = ["sender", "sender_message", "sender_date"]
#     search_fields = ["sender__username", "sender_date", "sender__email"]
#     list_display_links = ["sender"]

#     class Meta:
#         model = models.StepSupport
        
class StepSettingsAdmin(admin.ModelAdmin):
    search_fields = ["label", "value"]
    list_display = ["label", "value"]
    list_editable = ["value"]
    list_display_links = ["label"]
    class Meta:
        model = models.Settings

# admin.site.register(models.StepSupport, StepSupportAdmin)
admin.site.register(models.Settings, StepSettingsAdmin)
