from django.contrib import admin
from .models import AssignedCase, Report
# Register your models here.

admin.site.register([AssignedCase, Report])
