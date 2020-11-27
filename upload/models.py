from django.db import models

# Create your models here.
class Region(models.Model):

    id_region = models.AutoField(primary_key=True)
    cp = models.IntegerField()
    location = models.CharField(max_length=50) 
    country = models.TextField(max_length=50, default='SPAIN') 
    region = models.TextField(max_length=50, default='EUROPE') 
    latitude = models.TextField(max_length=50, default='NULL')
    longitude = models.TextField(max_length=50, default='NULL')
   
    class Meta:
        unique_together = ('cp','location')
    def __str__(self):
        return str(self.cp) +' '+ str(self.location)
    