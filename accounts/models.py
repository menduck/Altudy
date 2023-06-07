from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def get_emoji(exp):
    if exp >= 1000:
        return '🦖'
    elif exp >= 500:
        return '🦕'
    elif exp >= 200:
        return '🦎'
    elif exp >= 90:
        return '🐥'
    elif exp >= 30:
        return '🐣'
    elif exp >= 0:
        return '🥚'
    else:
        return ''


class User(AbstractUser):
    experience = models.PositiveIntegerField(default=0)


    def emoji_username(self):
        emoji = get_emoji(self.experience)
        return emoji + self.username


    def emoji(self):
        return get_emoji(self.experience)