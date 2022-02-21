from . import views
from django.urls import path


urlpatterns = [
    path("message/", views.add_message),
    path("message/get", views.get_report),
    path("message/<int:report_id>/", views.report_detail)
]
