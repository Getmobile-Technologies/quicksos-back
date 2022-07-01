from . import views
from django.urls import path


urlpatterns = [
    path("messages/assign/", views.assign),
    path("messages/assigned/", views.assigned_cases),
    path("messages/assigned/<uuid:assigned_case_id>/respond/", views.respond),
    path("messages/assigned/<uuid:assigned_case_id>/arrive/", views.has_arrived),
    path("messages/assigned/<uuid:assigned_case_id>/add_report/", views.add_report)
    
]
