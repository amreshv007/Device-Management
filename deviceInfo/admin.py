from django.contrib import admin
from .models import GivenTo, TakenFrom

admin.site.register(GivenTo)
admin.site.register(TakenFrom)