from django.db import models
from django.contrib.auth.models import User

class Concert(models.Model):
    concert_name = models.CharField(max_length=200)
    duration = models.DecimalField(max_digits=4, decimal_places=1)
    city = models.CharField(max_length=100)
    date = models.DateTimeField()
    def __str__(self):
        return self.concert_name

class ConcertAttending(models.Model):
    class AttendingChoices(models.TextChoices):
        NOTHING = '-', '-'
        NOT_ATTENDING = 'Not Attending', 'Not Attending'
        ATTENDING = 'Attending', 'Attending'
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='attendee')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attending = models.CharField(max_length=100, choices=AttendingChoices.choices, default='-')
    class Meta:
        unique_together = ['concert', 'user']
    def __str__(self):
        return self.attending

class Photo(models.Model):
    pic_url = models.URLField()
    event_country = models.CharField(max_length=100)
    event_state = models.CharField(max_length=100)
    event_city = models.CharField(max_length=100)
    event_date = models.CharField(max_length=30)
    class Meta:
        managed = False
    def __str__(self):
        return self.pic_url

class Song(models.Model):
    title = models.CharField(max_length=200)
    lyrics = models.TextField()
    class Meta:
        managed = False
    def __str__(self):
        return self.title
