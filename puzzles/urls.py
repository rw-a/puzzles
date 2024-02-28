from django.urls import path
from . import views

urlpatterns = [
    path("", views.puzzle_tree, name="puzzle_tree"),
]
