from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self,first_name, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),)

        user.first_name = email.split('@')[0]
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, first_name, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.first_name = email.split('@')[0]
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.first_name = email.split('@')[0]
        user.staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # an admin user; not a superuser
    is_admin = models.BooleanField(default=False)  # a superuser
    created_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name if self.first_name else self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name if self.first_name else self.email

    def __str__(self):
        return self.first_name if self.first_name else self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff
