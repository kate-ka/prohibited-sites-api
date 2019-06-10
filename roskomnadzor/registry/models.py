from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel

User = get_user_model()


class Registry(TimeStampedModel):
    ip = models.CharField(max_length=45, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.CharField(max_length=100)


class BlockRequest(TimeStampedModel):
    user_ip = models.CharField(max_length=45)
    site = models.URLField()
    description = models.CharField(max_length=100)
