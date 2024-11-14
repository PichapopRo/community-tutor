from django.db import models


class Event(models.Model):
    event_detail = models.CharField(max_length=200)
    start_date = models.DateTimeField("date published")



