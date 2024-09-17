from django.contrib import admin
from step.models import StepSupport

from django.contrib import admin
from .models import StepSupport

class StepSupportAdmin(admin.ModelAdmin):
    list_display = ["sender", "sender_message", "sender_date"]
    search_fields = ["sender__username", "sender_date", "sender__email"]
    list_display_links = ["sender"]

    class Meta:
        model = StepSupport

admin.site.register(StepSupport, StepSupportAdmin)