from .serializers import UserSerializer
from django.dispatch import receiver
# from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from config import settings
from rest_framework import serializers
from django.template.loader import render_to_string


domain = 'smartparcel.com'
url='#'
User = get_user_model()

# @receiver(post_save, sender=ResetPasswordOTP)
# def password_reset_token_created(sender, instance, created, *args, **kwargs):
#     if created:
#         code = instance.code
        
#         msg_html = render_to_string('forgot_password_otp.html', {
#                             'first_name': str(instance.user.first_name).title(),
#                             'code':code})
        
#         message= 'Hello {},\n\nYou are receiving this message because you or someone else have requested the reset of the password for your account.\nYour reset password code is:\n{}\n\nPlease if you did not request this please ignore this e-mail and your password would remain unchanged. OTP expires in 5 minutes.\n\nRegards,\nSmart Parcel Team'.format(instance.user.first_name, code)
        
#         send_mail(
#             subject = "RESET PASSWORD OTP FOR SAMRT PARCEL",
#             message= message,
#             html_message=msg_html,
#             from_email  = 'SMART PARCEL SUPPORT <noreply@smartparcel.com>',
#             recipient_list= [instance.email]
#         )
    
    
@receiver(post_save, sender=User)
def send_otp(sender, instance, created, **kwargs):
    if created:
        print(instance.password)
        subject = f"YOUR {instance.role} ACCOUNT FOR QUICKSOS".upper()
        
        message = f"""Hi, {str(instance.first_name).title()}.
You have just been onboarded on the quicksos platform. Your login details are below:
E-mail: {instance.email} 
password: {instance.password}           
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
        print(instance.password)
        return
    
    
    