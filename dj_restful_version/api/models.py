from django.db import models


class UserGroup(models.Model):
    title = models.CharField(max_length=32)


class UserInfo(models.Model):
    USER_TYPE_CHOICES = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)

    group = models.ForeignKey("UserGroup")
    roles = models.ManyToManyField("Role")


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo')
    token = models.CharField(max_length=64)


class Role(models.Model):
    title = models.CharField(max_length=32)
