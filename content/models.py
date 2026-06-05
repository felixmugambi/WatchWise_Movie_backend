from django.db import models
from django.conf import settings

class Content(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    genres = models.JSONField(default=list) # Store genre IDs or names
    runtime = models.IntegerField(null=True, blank=True) # minutes
    media_type = models.CharField(max_length=10, choices=[("movie", "Movie"), ("tv", "TV")])
    
    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ("tmdb_id", "media_type")

class WatchEntry(models.Model):
    STATUS_CHOICES = [
        ('PLAN', 'Plan to Watch'),
        ('WATCHING', 'Watching'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
        ('WAITING', 'Waiting to be Released'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist')
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLAN')
    rating = models.IntegerField(null=True, blank=True) # 1-5
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'content')

    def __str__(self):
        return f"{self.user.first_name} - {self.content.title} ({self.status})"
