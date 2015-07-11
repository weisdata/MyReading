from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    summary = models.TextField()
    link = models.CharField(max_length=2000)
    source = models.CharField(max_length=2000, blank=True)
    image = models.CharField(max_length=2000, blank=True)
    READ = 'RD'
    UNREAD = 'UD'
    STATUS_CHOICES = (
        (READ, 'Read'),
        (UNREAD, 'Unread'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=UNREAD)
    published_date = models.DateTimeField(
            default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username



