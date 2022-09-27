#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings #장고가 관리하는 세팅에서 불러와줘

# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followee') # 사용자가 사용자를 팔로우
      # 내가 팔로우 하는 사람들 = follow ,  내가 팔로우 한 사람들 입장에서 나는 followee