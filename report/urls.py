from . import views
from django.urls import path


urlpatterns = [
    path("messages/assign/", views.assign),
    path("messages/assigned/", views.assigned_cases),
    path("messages/assigned/<uuid:assigned_case_id>/respond/", views.respond),
    path("messages/assigned/<uuid:assigned_case_id>/arrive/", views.has_arrived),
    path("messages/assigned/<uuid:assigned_case_id>/add_report/", views.add_report),
    path("messages/report-history/", views.report_history),
    path("request-backups/", views.request_backup),
    path("request-backups/all/", views.requested_backups),
    path("request-backups/<uuid:request_id>/approve/", views.respond_to_request),
    
]
