from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from accounts.serializers import User
from config import settings
from rest_framework import serializers
from django.template.loader import render_to_string
from main.models import Message, Agency
from main.helpers.push_notifications import send_push_notification
from report.models import AssignedCase
from report.serializers import AssignedCaseSerializer
from main.helpers.firebase_store import send_mobile_notification

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
        
        # escalators =[b.members.filter(role="escalator").values_list("email", flat=True) for b in instance.emergency_code.agency.all() if instance.emergency_code] 
        
#         subject = f"New Emergency Escalated"
        
#         message = f"""Hello,
# A new emergency has just been escalated to you. Quickly respond to this immediately.

# Cheers,
# QuickSOS Team.       
# """   
        # msg_html = render_to_string('signup_email.html', {
        #                 'first_name': str(instance.first_name).title(),
        #                 'code':code,
        #                 'url':url})
        
        # email_from = settings.Common.DEFAULT_FROM_EMAIL
        # recipient_list = get_data(escalators)
        # send_mail( subject, message, email_from, recipient_list)
        
        # print(recipient_list)
        # print(instance.password)
        
        agency_ids =  instance.emergency_code.all().values_list('agency', flat=True)

        agencies = Agency.objects.filter(uuid__in=agency_ids)

        escalator_keys = get_data([agency.members.filter(role="escalator").values_list("firebase_key", flat=True) for agency in agencies]) 

        for key in escalator_keys:
            send_push_notification("escalated", key)
        
        
        return
    
    
    

# @receiver(post_save, sender=Message)
# def send_agent_notification(sender, instance, created, **kwargs):
#     if created:
#         agents =User.objects.filter(role="agent")
        
#         subject = f"New Emergency Escalated"
        
#         message = f"""Hello,
# A case was just been report to you. Login to your dashboard to escalate it immediately.

# Cheers,
# QuickSOS Team.       
# """   
#         # msg_html = render_to_string('signup_email.html', {
#         #                 'first_name': str(instance.first_name).title(),
#         #                 'code':code,
#         #                 'url':url})
        
#         email_from = settings.Common.DEFAULT_FROM_EMAIL
#         recipient_list = agents.values_list("email", flat=True)
#         send_mail(subject, message, email_from, recipient_list)
        
#         # print(recipient_list)
#         # print(instance.password)
#         agent_keys =agents.values_list("firebase_key", flat=True)
        
#         for key in agent_keys:
#             send_push_notification("new_case", key)
        
        
#         return
    
    
@receiver(post_save, sender=AssignedCase)
def send_responder_notification(sender,instance, created, **kwargs):
    if created:
        send_mobile_notification(instance.responder.id)
        
        
        
        
    return
    