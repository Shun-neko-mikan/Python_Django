from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    account_image = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username

class DLurls(models.Model):
    website = models.URLField(max_length=400)

