from django.urls import path
from . import views

urlpatterns = [
    path("", views.puzzle_tree, name="puzzle_tree"),
    path("journal/<str:identifier>/", views.puzzle_view, name="puzzle_view"),
]
