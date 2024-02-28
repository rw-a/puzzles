from django.db import models
from django.db.models.indexes import Index


class Puzzle(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        indexes = (
            Index(fields=['identifier']),
        )
        ordering = ('identifier',)


class Hint(models.Model):
    description = models.TextField()
    order = models.IntegerField()
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)

    class Meta:
        indexes = (
            Index(fields=['puzzle', 'order']),
        )
        ordering = ['puzzle', 'order']
