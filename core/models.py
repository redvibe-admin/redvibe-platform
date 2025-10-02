from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.creator.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
