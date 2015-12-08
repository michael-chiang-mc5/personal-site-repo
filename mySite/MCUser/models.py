from django.db import models
from django.contrib.auth.models import User

class MCUserProfile(models.Model):
    user = models.ForeignKey(User)
