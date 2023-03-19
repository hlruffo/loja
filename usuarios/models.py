from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    choices_cargo = (('V', 'Vendendor'),
                     ('G', 'Gerente'))
    cargo = models.CharField(choices=choices_cargo, max_length=1)
