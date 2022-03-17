from . import views
from django.urls import path


urlpatterns = [
    path("messages/", views.add_message),
    path("messages/get", views.get_message),
    path("messages/<uuid:message_id>/escalate/", views.escalate),
    path("messages/<uuid:message_id>/", views.message_detail),
    path("agencies/", views.agencies),
    path("agencies/<uuid:agency_id>/", views.agency_detail),
    path("agencies/escalated/", views.escalated_message)
    
]
