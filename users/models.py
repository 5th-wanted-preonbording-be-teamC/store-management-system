from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    """
    BaseUserManager : User를 생성할때 사용하는 클래스
    """

    def create_user(self, user_id, password, **extra_fields):
        """
        User 생성하는 함수
        """
        if not user_id:
            raise ValueError(_("The Email must be set"))
        user_id = self.normalize_email(user_id)
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_id, password, **extra_fields):
        """
        관리자 User 생성하는 함수수"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(user_id, password, **extra_fields)


class User(AbstractUser):
    """
    AbstractUser : 상속받아 생성하는 클래스
    """

    first_name = None
    last_name = None
    password = models.CharField(max_length=20, null=False, verbose_name="비밀번호")
    user_name = models.CharField(max_length=30, null=False, verbose_name="사용자 이름")
    address = models.CharField(max_length=100, blank=True, verbose_name="주소")

    objects = UserManager()

    REQUIRED_FIELDS = []
