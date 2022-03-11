from django.contrib import admin
from .models import Message, Escalator
# Register your models here.


admin.site.register([Message, Escalator])
