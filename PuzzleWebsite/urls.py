from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='admin/login.html',
        extra_context={
            'site_header': "Journal",
        })),
    path('admin/', admin.site.urls),
    path('', include("puzzles.urls"))
]
