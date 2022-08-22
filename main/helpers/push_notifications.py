from firebase_admin import messaging
from django.utils import timezone
from pathlib import Path

def send_notification(notice_for, user):
    
    # firebase_key = user.firebase_key
    firebase_key = user.firebase_key
    
    if notice_for == "new_case":
        title = 'New Emergency'
        body = "Hurry! A new emergency occurred."
    elif notice_for == "escalated":
        title = 'Escalated Emergency'
        body = "Hurry! A new emergency has was just escalated."
    elif notice_for == "assigned_case":
        title = 'New case assigned'
        body = "Hurry! A new case has been assigned to you"
        
    elif notice_for == "new_request":
        title = 'New request'
        body = "New message requesting for backup."
        
    else:
        title = ""
        body=""
    
    message = messaging.Message(
        token=firebase_key,
        notification=messaging.Notification(
            title=title,
            body=body,
            ),
        data={
            'message':body
            }
        )
    
    try:
        response = messaging.send(message)
        print(response.json())
    except Exception as e:
        pass
        

    
