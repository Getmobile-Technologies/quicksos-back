from django.db import models
import uuid
from django.contrib.auth import get_user_model
from accounts.models import phone_regex
from django.utils import timezone
# Create your models here.

User = get_user_model()
class Agency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(unique=True, max_length=255)
    acronym = models.CharField(unique=True, max_length=255)
    is_active= models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]
    
    def __str__(self) -> str:
        return self.acronym
    
    def delete(self):
        self.is_active=False
        self.save()
        
        self.members.all().update(is_active=False) #deactivate all users associated with this escalator i.e first responders and admin
        self.members.save()
        
        return
    
class Message(models.Model):
    STATUS = (("pending", "Pending"),
              ("escalated", "Escalated"),
              ("assigned", "Assigned"),
              ("completed", "Completed")
              )
    
    PROVIDERS = (("whatsapp", "Whatsapp"), 
                 ("call", "Call"))
    
    CATEGORY_CHOICES = (("emergency", "Emergency"),
                        ("non_emergency", "Non-Emergency"),
                        ("hoax", "Hoax"))
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=300)
    phone = models.CharField(max_length=15,  validators=[phone_regex])
    status = models.CharField(max_length=300, default="pending", choices=STATUS)
    address = models.TextField(null=True,blank=True)
    category = models.CharField(max_length=100, blank=True, null=True, choices=CATEGORY_CHOICES)
    agent = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    emergency_code = models.ForeignKey("main.EmergencyCode", related_name="emergency_codes", blank=True, on_delete=models.CASCADE, null=True)
    local_gov = models.CharField(max_length=250, blank=True, null=True)
    agent_note = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_escalated = models.DateTimeField(null=True)
    provider = models.CharField(max_length=255, default="whatsapp", choices=PROVIDERS)
    is_active=models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ["-date_created"]

    def __str__(self) -> str:
        return self.name
    
    @property
    def response_data(self):
        return self.answers.filter(is_active=True).values("answer",'question__question')
    
    @property
    def issue(self):
        return self.answers.first().question.issue.name
    
    @property
    def agency_detail(self):
        return self.emergency_codes.agency.values("acronym")
    
    def delete(self):
        self.is_active=False
        self.save()
        


    
class Issue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=250, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def question_list(self):
        return self.questions.filter(is_active=True).values("id", "question", "is_image")
    
    @property
    def case_count(self):
        today = timezone.now().date()
        messages = Message.objects.filter(is_active=True, date_created__date=today)
        total = len(list(filter(lambda message : message.answers.first().question.issue.id == self.id, messages)))
        return total
    
    
    def delete(self):
        self.is_active=False
        self.questions.update(is_active=False)
        self.save()
        
        
class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    question = models.CharField(max_length=250)
    issue = models.ForeignKey("main.Issue", on_delete=models.CASCADE, related_name="questions", null=True)
    is_image = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return f"{self.question} ---> {self.issue.name}"
    
    
    def delete(self):
        self.is_active=False
        self.answers.update(is_active=False)
        self.save()
        
        
class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey("main.Question", on_delete=models.CASCADE, related_name="answers")
    message = models.ForeignKey("main.Message", on_delete=models.CASCADE, related_name="answers")
    answer = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return f"{self.answer} ---> {self.message.name}"
    
    
    def delete(self):
        self.is_active=False
        self.save()
        
        
class EmergencyCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(max_length=255, unique=True)
    agency = models.ManyToManyField("main.agency", related_name="codes")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
   
    def __str__(self):
        return self.code
    
    
    def delete(self):
        self.is_active=False
        self.save()