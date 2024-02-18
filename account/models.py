from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, Fname,Lname, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            Fname=Fname,
            Lname =Lname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, Fname,Lname, password=None):
        user = self.create_user(email, Fname=Fname, Lname = Lname, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    Fname = models.CharField(max_length=200,blank=True)
    Lname = models.CharField(max_length=200,blank=True)
   
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Fname','Lname']

    def __str__(self):
        return self.email
