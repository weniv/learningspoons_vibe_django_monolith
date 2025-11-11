# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="닉네임"
    )
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True, verbose_name="프로필 이미지"
    )
    bio = models.TextField(blank=True, null=True, verbose_name="자기소개")

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        """닉네임이 있으면 닉네임, 없으면 username 반환"""
        return self.nickname if self.nickname else self.username
