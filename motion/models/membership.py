from django.db import models

class Membership(models.Model):
    name = models.CharField(max_length=50)
    limit = models.IntegerField() # Limit kelas perminggu 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField() 

    def __str__(self):
        return self.name