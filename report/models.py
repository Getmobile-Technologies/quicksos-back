import uuid
from django.db import models
from django.contrib.auth import get_user_model
from main.models import Message

User=get_user_model()
# Create your models here.

class AssignedCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_cases")
    case = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="assigned")
    escalator_note = models.TextField(null=True, blank=True)
    status = models.CharField(default="pending", max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return self.case
    
    @property
    def report_detail(self):
        return self.reports.all().values("situation_report", "image_url1", "image_url2")
    
    def delete(self):
        self.is_active=False
        self.save()
        self.reports.all().update(is_active=False)

    
class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    assigned_case = models.ForeignKey(AssignedCase, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    situation_report = models.TextField()
    image_url1 = models.URLField(null=True, blank=True)
    image_url2 = models.URLField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return self.case
    
    
    def delete(self):
        self.is_active=False
        self.save()