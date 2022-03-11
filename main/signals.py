from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from config import settings
from rest_framework import serializers
from django.template.loader import render_to_string
from main.models import Message

domain = 'quicksos.com'
url='#'

def get_data(queryset):
    flattened = []
    for data in queryset:
        for i in data:
            flattened.append(i)
            
    return flattened
        
    
    
@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if instance.status=="escalated":
        escalators =[b.members.filter(role="escalator").values_list("email", flat=True) for b in instance.escalators.all()] 
        
        subject = f"New Emergency Escalated"
        
        message = f"""Hello,
A new emergency has just been escalated to you. Quickly respond to this immediately.

Cheers,
QuickSOS Team.       
"""   
        # msg_html = render_to_string('signup_email.html', {
        #                 'first_name': str(instance.first_name).title(),
        #                 'code':code,
        #                 'url':url})
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = get_data(escalators)
        send_mail( subject, message, email_from, recipient_list)
        
        print(recipient_list)
        # print(instance.password)
        return
    
    
    