from django.contrib import admin
from .models import EmergencyCode, Message, Agency, Issue, Question, Answer
# Register your models here.


admin.site.register([ Agency, Issue,EmergencyCode])


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['issue']
    
    
    
class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    inlines = [AnswerInline]