from django.urls import path, include
from . import views


urlpatterns = [
    path("users/add/", views.add_user),
    path('user/forget_password/', include('django_rest_passwordreset.urls', namespace='forget_password')),
]
