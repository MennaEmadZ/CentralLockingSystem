from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    locked_by = models.CharField(max_length=100, null=True, blank=True)
    ttl = models.PositiveIntegerField(null=True, blank=True)
    timeout = models.PositiveIntegerField(null=True, blank=True)