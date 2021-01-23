from django.contrib import admin
from .models import Events, Participants,Account
# Register your models here.
admin.site.register(Events)
admin.site.register(Participants)
admin.site.register(Account)