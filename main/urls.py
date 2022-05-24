from . import views
from django.urls import path


urlpatterns = [
    path("message/", views.add_message),
    path("messages/all", views.get_message),
    path("messages/pending", views.peding_message),
    path("messages/<uuid:message_id>/escalate/", views.escalate),
    path("messages/<uuid:message_id>/report/", views.message_report),
    path("messages/escalated/", views.escalated_message),
    path("messages/<uuid:message_id>/", views.message_detail),
    path("messages/<uuid:message_id>/mark_as_emergency/", views.mark_as_emergency),
    path("agencies/", views.agencies),
    path("agencies/<uuid:agency_id>/", views.agency_detail),   
]
