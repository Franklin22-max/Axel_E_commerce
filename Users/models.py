from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from PIL import Image



class CustomAccountManager(BaseUserManager):
    def create_superuser(self,email,username,phone,password,**otherfields):
        otherfields.setdefault('is_staff',True)
        otherfields.setdefault('is_superuser',True)

        if otherfields.get('is_staff') is not True:
            raise ValueError(
                "superuser must have is_staff=True"
            )
        if otherfields.get('is_superuser') is not True:
            raise ValueError(
                "superuser must have is_superuser=True"
            )
        return self.create_user(email,username,phone,password,**otherfields)
    
    def create_user(self,email,username,phone,password,**otherfields):
        if not email:
            raise ValueError(
                _('email must be assigned')
            )
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone ,**otherfields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField( unique=True)
    username = models.CharField(max_length=200, unique=True)
    phone = models.IntegerField(blank=True)
    profile_img = models.ImageField(default='default.png', upload_to='profile_pics')
    gender = models.CharField(max_length=7, choices=[('M','Male'),('F','Female'),('O','Others')], default=('O','Others'))

    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone', 'gender']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_img.path)

        if(img.height > 300 or img.width > 300):
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
