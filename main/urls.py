from . import views
from django.urls import path


urlpatterns = [
    path("messages/", views.add_message),
    path("messages/get", views.get_message),
    path("messages/<uuid:message_id>/escalate/", views.escalate),
    path("messages/<uuid:message_id>/", views.message_detail),
    path("escalators/", views.escalators),
    path("escalators/<uuid:escalator_id>/", views.escalator_detail),
    path("escalators/escalated/", views.escalated_message)
    
]
