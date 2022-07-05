import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from main.models import Message


User=get_user_model()
# Create your models here.

class AssignedCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_cases")
    case = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="assigned")
    escalator_note = models.TextField(null=True, blank=True)
    status = models.CharField(default="pending", max_length=200)
    responded = models.BooleanField(default=False)
    arrived = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ["-date_created"]
    
    def __str__(self) -> str:
        return f"{self.case.name} -- {self.responder.agency.acronym}"
    
    @property
    def report_detail(self):
        return self.reports.all().values("situation_report", "image_url1", "image_url2")
    
    @property
    def case_detail(self):
        return model_to_dict(self.case, exclude="agencies")
    
    @property
    def issue(self):
        return self.case.answers.all().first().question.issue.name
    
    @property
    def img_url(self):
        for response in self.case.answers.all():
            if response.question.is_image ==True:
                return response.answer
        return ""
    
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
    
    class Meta:
        ordering = ["-date_created"]
    
    def __str__(self) -> str:
        return self.assigned_case.responder.agency.acronym
    
    
    def delete(self):
        self.is_active=False
        self.save()
        
        
        
class RequestSupport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    case = models.ForeignKey("main.Message", on_delete=models.CASCADE, related_name="requested_support")
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="requested_support", null=True, blank=True)
    assignment = models.ForeignKey(AssignedCase, on_delete=models.CASCADE, related_name="requested_support")
    agencies = models.ManyToManyField('main.Agency', related_name="requested_support")
    status = models.CharField(max_length=250, default="pending")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    class Meta:
        ordering = ["-date_created"]
    
    def __str__(self) -> str:
        return f"Request by {self.sender.email}"
    
    @property
    def case_detail(self):
        return self.case
    
    @property
    def agency_detail(self):
        return self.agencies
    
    @property
    def sender_detail(self):
        return {"local_gov":self.sender.local_gov, "agency":self.sender.agency.acronym}
    
    def delete(self):
        self.is_active=False
        self.save()
    
    
    
    
    