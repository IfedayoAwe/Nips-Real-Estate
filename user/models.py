from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            return ValueError("Users must have an email address")
        if not name:
            return ValueError("Users must have a name")

        user = self.model(
            email=self.normalize_email(email).lower(),
            name=name,
            password = password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_realtor(self, email, name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            name = name,
        )
        user.is_realtor = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            name = name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_realtor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = MyAccountManager()

    def __str__(self):
        return self.email