from firebase import firebase
import os

def send_to_db():
    """Sends a notification to the firebase database for the mobile app"""
    user_id = "4ed99221-03f2-4e3b-88d4-8f16dad082cd"
    connect = firebase.FirebaseApplication(os.getenv("FIREBASE_DB_URL"))
    result = connect.post(f'/notifications/{user_id}', data={
        "body": "The act is awesome",
        "title":"new alert",
    })

    return 


# def get_from_db():
    
    
    
#     connect = firebase.FirebaseApplication(os.getenv("FIREBASE_DB_URL"))
#     result = connect.get('/notifications', None)
#     print(result)

#     return 