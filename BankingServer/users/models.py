from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

# Create your models here.

class UserManager(DjangoUserManager):
    def _create_user(self, name, user_id, password=None, **extra_fields):
        # 아이디 필수 입력
        if not user_id:
            raise ValueError('아이디는 필수 값입니다.')

        # 아이디 중복 체크
        if self.model.objects.filter(user_id=user_id).exists():
            raise ValueError('이미 사용 중인 아이디입니다.')

        user = self.model(name=name, user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, user_id, password, **extra_fields)

    def create_superuser(self, name, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, user_id, password, **extra_fields)


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=20, unique=True, verbose_name='이름', null=True, default='default_value_here')
    user_id = models.CharField(max_length=20, unique=True, verbose_name='아이디', default='default_value_here')
    email = models.EmailField(blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'user_id'  # username 대신 user_id을 사용
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name