from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    """お気に入り店舗"""
    shop_id = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.shop_id

