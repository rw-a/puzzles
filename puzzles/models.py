from django.db import models


class Puzzle(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)


class Hint(models.Model):
    description = models.TextField()
    order = models.IntegerField()
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
