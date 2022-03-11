from django.db import models
import uuid
# Create your models here.

class Escalator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(unique=True, max_length=255)
    acronym = models.CharField(unique=True, max_length=255)
    is_active= models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
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
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=300)
    issue = models.TextField()
    address = models.TextField(null=True,blank=True)
    image_url1 = models.URLField()
    image_url2 = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=300, default="pending", choices=STATUS)
    escalators =  models.ManyToManyField(Escalator, related_name="messages", blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    
    
    def __str__(self) -> str:
        return self.issue
    
    
    def delete(self):
        self.is_active=False
        self.save()
        


    
        