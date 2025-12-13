from django.contrib import admin
from django.urls import path, include
from views import views

urlpatterns = [
    # Django built-in admin site restored to the default path
    path("admin/", admin.site.urls),
    # Authentication URLs (login/logout) for staff access
    path('accounts/', include('django.contrib.auth.urls')),
    # Application routes (including staff-admin/ paths)
    path("", include("views.urls")),
]
