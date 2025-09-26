from django.db import models

# Create your models here.
class Alumni(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    graduation_year = models.IntegerField()
    profession = models.CharField(max_length=100, blank=True, null=True)
    work_history = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.graduation_year})"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title