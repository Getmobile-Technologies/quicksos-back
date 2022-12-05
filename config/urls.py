from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import authentication # new
from accounts import permissions
from drf_yasg.views import get_schema_view # new
from drf_yasg import openapi 
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="QuickSOS",
        default_version="v1",
        description="API for QuickSOS",
        terms_of_service="",
        contact=openapi.Contact(email="desmond@getmobile.tech"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=(authentication.BasicAuthentication,)
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/account/', include('accounts.urls')),
    path("v1/", include("main.urls")),
    path("v1/", include("report.urls")),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
