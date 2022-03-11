import uuid
from django.db import models
from django.contrib.auth import get_user_model
from main.models import Message

User=get_user_model()
# Create your models here.

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    case = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="reports")
    escalator_note = models.TextField(null=True, blank=True)
    situation_report = models.TextField(null=True, blank=True)
    image_url1 = models.URLField(null=True, blank=True)
    image_url2 = models.URLField(null=True, blank=True)
    status = models.CharField(default="pending", max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return self.case
    
    
    def delete(self):
        self.is_active=False
        self.save()
    