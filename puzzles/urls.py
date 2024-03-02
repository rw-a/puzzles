from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.puzzle_tree, name="puzzle_tree"),
    # path('media/<str:file_path>/', views.media, name="media"),
    path("journal/<str:identifier>/", views.puzzle_view, name="puzzle_view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
