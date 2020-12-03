from django.db import models

# Create your models here.
class Status(models.Model):
    status_choices = [
        ('O', 'OnGoing'),
        ('C', 'Completed'),
        ('S', 'Stored'),
        ('F', 'Failed'),
    ]
    id_task = models.CharField(max_length=40, primary_key=True)
    command = models.TextField(max_length=50)
    status = models.CharField(max_length=20, choices=status_choices)
    date = models.DateTimeField()
    elapsed_time = models.IntegerField()

    def __str__(self):
        return str(self.id_task)