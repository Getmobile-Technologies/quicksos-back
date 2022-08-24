from . import views
from django.urls import path


urlpatterns = [
    path("message/", views.add_message),
    path("messages/all", views.get_message),
    path("messages/pending", views.pending_message),
    path("messages/<uuid:message_id>/escalate/", views.escalate),
    path("messages/<uuid:message_id>/report/", views.message_report),
    path("messages/escalated/", views.escalated_message),
    path("messages/<uuid:message_id>/", views.message_detail),
    path("messages/<uuid:message_id>/mark_as_emergency/", views.mark_as_emergency),
    path("agencies/", views.agencies),
    path("agencies/<uuid:agency_id>/", views.agency_detail),   
    path("issues/", views.issues),
    path("issues/<uuid:issue_id>/", views.issue_detail),
    path("questions/<uuid:question_id>/", views.question_detail),  
    path("dashboard/", views.dashboard_view)
]
