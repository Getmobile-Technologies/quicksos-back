from .serializers import UserSerializer
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from config import settings
from rest_framework import serializers
from django.template.loader import render_to_string


domain = 'quicksos.com'
url='#'
User = get_user_model()

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    token = "https://{}/forgot-password/{}".format(domain,reset_password_token.key)
    
    # msg_html = render_to_string('forgot_password_otp.html', {
    #                     'first_name': str(instance.user.first_name).title(),
    #                     'code':code})
    
    message= 'Hello {},\n\nYou are receiving this message because you or someone else have requested the reset of the password for your account.\nKindly follow tis link or copy it to your browser to change your password:\n{}\n\nPlease if you did not request this please ignore this e-mail and your password would remain unchanged.\n\nRegards,\nQuick SOS Support'.format(instance.user.first_name, token)
    
    send_mail(
        subject = "RESET PASSWORD OTP FOR QUICK SOS",
        message= message,
        # html_message=msg_html,
        from_email  = 'QUICK SOS <noreply@quicksos.com>',
        recipient_list= [instance.email]
    )
    
    
@receiver(post_save, sender=User)
def send_details(sender, instance, created, **kwargs):
    if created and instance.is_superuser==False:
        # print(instance.password)
        role = " ".join(str(instance.role).split('_'))
        subject = f"YOUR {role} ACCOUNT FOR QUICKSOS".upper()
        
        message = f"""Hi, {str(instance.first_name).title()}.
You have just been onboarded on the quicksos platform. Your login details are below:
E-mail: {instance.email} 
password: {instance.password}    

Cheers,
QuickSOS Team.       
"""   
        # msg_html = render_to_string('signup_email.html', {
        #                 'first_name': str(instance.first_name).title(),
        #                 'code':code,
        #                 'url':url})
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail( subject, message, email_from, recipient_list)
        
        instance.set_password(instance.password)
        instance.save()
        # print(instance.password)
        return
    
    
    