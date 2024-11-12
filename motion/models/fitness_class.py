from django.db import models

class FitnessClass(models.Model):
    name = models.CharField(max_length=50)
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_participants = models.IntegerField(default=10)
    members = models.ManyToManyField('Member', blank=True)

    def __str__(self):
        return self.name
