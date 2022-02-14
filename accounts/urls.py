from django.urls import path
from . import views


urlpatterns = [
    path("users/add/", views.add_user)
]
