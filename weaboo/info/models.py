from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    def __str__(self) -> str:
        return self.username
    

class ListType(models.Model):
    list_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.list_name
    

class UserShowList(models.Model):
    user = models.ManyToManyField(CustomUser, related_name="user_show_list")
    list = models.ManyToManyField(ListType, related_name="user_show_list")
    mal_id = models.IntegerField()
    episode_watched = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.mal_id}"