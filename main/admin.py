from django.contrib import admin
from .models import Message, Agency
# Register your models here.


admin.site.register([Message, Agency])
