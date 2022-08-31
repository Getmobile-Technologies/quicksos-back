from django.contrib import admin
from .models import EmergencyCode, Message, Agency, Issue, Question, Answer
# Register your models here.


admin.site.register([Message, Agency, Issue, Question, Answer, EmergencyCode])
