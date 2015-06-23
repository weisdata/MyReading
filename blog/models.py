from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    summary = models.TextField()
    link = models.CharField(max_length=2000)
    source = models.CharField(max_length=2000, blank=True)
    image = models.CharField(max_length=2000, blank=True)
    published_date = models.DateTimeField(
            default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

