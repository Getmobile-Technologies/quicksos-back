from django.db import models
import uuid
from django.contrib.auth import get_user_model
from accounts.models import phone_regex
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
    
    CATEGORY_CHOICES = (('rape', 'Rape'), ('child_abuse', 'Child Abuse'), ('domestic_violence', 'Domestic Violence'), ('missing_person', 'Missing Person'), ('dead_body', 'Dead Body'), ('collapsed_building', 'Collapsed Building'), ('accident', 'Accident'), ('fight', 'Fight'), ('fire_outbreak', 'Fire Outbreak'))
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_of_reporter = models.CharField(max_length=300)
    phone = models.CharField(max_length=15,  validators=[phone_regex])
    victim_name = models.CharField(max_length=300, null=True,blank=True)
    victim_gender = models.CharField(max_length=300, null=True,blank=True)
    victim_age = models.CharField(max_length=300, null=True,blank=True)
    status = models.CharField(max_length=300, default="pending", choices=STATUS)
    category = models.CharField(max_length=300, choices=CATEGORY_CHOICES)
    description = models.TextField()
    address = models.TextField(null=True,blank=True)
    incident_address = models.TextField(null=True,blank=True)
    image_url1 = models.URLField(null=True, blank=True)
    image_url2 = models.URLField(null=True, blank=True)
    additional_info = models.TextField(null=True,blank=True)
    last_seen_detail = models.TextField(null=True,blank=True)
    is_emergency = models.BooleanField(default=False)
    
    agent = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    agencies =  models.ManyToManyField(Agency, related_name="messages", blank=True)
    agent_note = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=255, default="whatsapp", choices=PROVIDERS)
    
    is_active=models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ["-date_created"]

    def __str__(self) -> str:
        return self.issue
    
    
    def delete(self):
        self.is_active=False
        self.save()
        


    
# a = ["RAPE", "CHILD ABUSE", "DOMESTIC VIOLENCE", "ENQUIRY", "MISSING PERSON", "DEAD BODY", "COLLAPSED BUILDING", "ACCIDENT","FIGHT",  "FIRE OUTBREAK"]

# b = []
# for i in a:
#     b.append((i.lower(), i.title()))
# print(b)
        