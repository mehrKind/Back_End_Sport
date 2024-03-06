from django.contrib import admin
from .models import ContactUs_db


@admin.register(ContactUs_db)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_textBody', 'send_date',)  # add other fields if needed
    search_fields = ('textBody',)

    def short_textBody(self, obj):
        return f"{obj.textBody[:19]} ..."  # adjust the number as needed

    short_textBody.short_description = 'user_Message'  # this is the column title
