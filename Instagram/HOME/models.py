from django.db import models

# Create your models here.
class APPLIST(models.Model):
    # db_table = "APPLIST"
    APPNAME = models.CharField(max_length=100)
    APPURL = models.CharField(max_length=100)

    def __str__(self):
        ret = self.APPNAME
        return ret