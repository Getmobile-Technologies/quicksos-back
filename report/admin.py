from django.contrib import admin
from .models import AssignedCase, Report, RequestSupport
# Register your models here.

admin.site.register([AssignedCase, Report, RequestSupport])