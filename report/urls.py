from . import views
from django.urls import path


urlpatterns = [
    path("messages/assign/", views.assign)
    
]
