from django.contrib import admin
from puzzles.models import Hint, Puzzle


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'name', 'password', 'date', 'parent')


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('puzzle', 'order', 'description')
