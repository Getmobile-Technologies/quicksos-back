from django.urls import path, include
from . import views


urlpatterns = [
    path("users/add/", views.add_admin),
    path("users/agents/", views.get_agents),
    path("users/escalators/", views.get_escalators),
    path("users/profile/", views.user_detail),
    path("users/<uuid:user_id>/", views.get_user_detail),
    path("users/auth/", views.user_login),
    path("users/reset_password/", views.reset_password),
    
    path('users/forget_password/', include('django_rest_passwordreset.urls', namespace='forget_password')),
]
