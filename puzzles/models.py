from django.contrib.auth.models import User
from django.db import models
from django.db.models.indexes import Index


class Puzzle(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    password_type = models.CharField(max_length=10, choices=[
        ('letters', 'letters'),
        ('numbers', 'numbers')
    ])
    text = models.TextField()
    date = models.DateTimeField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        indexes = (
            Index(fields=['identifier']),
        )
        ordering = ('identifier',)
        
    def __str__(self):
        return f"[{self.identifier}] {self.name}"


class Hint(models.Model):
    description = models.TextField()
    order = models.IntegerField()
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)

    class Meta:
        indexes = (
            Index(fields=['puzzle', 'order']),
        )
        ordering = ['puzzle', 'order']
    
    def __str__(self):
        return f"Hint {self.order} for {str(self.puzzle)}"


class Solve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solved = models.JSONField(default=list, blank=True, null=True)
    
    def __str__(self):
        return f"User {self.user} solved {self.solved}"
