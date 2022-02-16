from . import views
from django.urls import path


urlpatterns = [
    path("message/", views.add_message)
]
