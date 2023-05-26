from firebase import firebase
import os

def send_mobile_notification(user_id):
    """Sends a notification to the firebase database for the mobile app"""
    


    connect = firebase.FirebaseApplication(os.getenv("FIREBASE_DB_URL"))
    result = connect.patch(f'/notifications/{user_id}', data={
        "body": "Hurry! A new case has been assigned to you",
        "title":"New case assigned",
    })
    
    

    return 

