from django.db import models
import uuid
from django.utils import timezone

# Create your models here.


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
