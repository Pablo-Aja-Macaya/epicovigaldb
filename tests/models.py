from django.db import models
from tests.tasks import check_status


### CLASSES ###
class PicardTests(models.Model):
    id_test = models.AutoField(primary_key=True)
    id_process = models.IntegerField()
    mean_target_coverage = models.DecimalField(max_digits=15, decimal_places=6) 
    median_target_coverage = models.DecimalField(max_digits=15, decimal_places=6) 
    pct_target_bases_1x = models.DecimalField(max_digits=7, decimal_places=6) 
    pct_target_bases_10x = models.DecimalField(max_digits=7, decimal_places=6) 
    pct_target_bases_100x = models.DecimalField(max_digits=7, decimal_places=6) 

    def __str__(self):
        return str(self.id_process)


### Functions ###
def prueba():
    check_status.delay()

