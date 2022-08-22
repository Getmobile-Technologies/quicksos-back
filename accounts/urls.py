from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("users/add/", views.add_admin),
    path("users/agents/", views.get_agents),
    path("users/escalators/", views.get_escalators),
    path("users/first_responders/", views.get_responders),
    path("users/profile/", views.user_detail),
    path("users/<uuid:user_id>/", views.get_user_detail),
    path("users/auth/", views.user_login),
    path('users/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("users/reset_password/", views.reset_password),
    path("users/change_firebase_key", views.change_firebase_key),
    path('users/forget_password/', include('django_rest_passwordreset.urls', namespace='forget_password')),
]
