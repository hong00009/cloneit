from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Movie

# Create your models here.
class User(AbstractUser):
    pass
    