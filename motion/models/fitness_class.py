from django.db import models

class FitnessClass(models.Model):
    name = models.CharField(max_length=50)
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    room = models.CharField(max_length=100, choices=[
        ("Studio 1", "Studio 1"),
        ("Studio 2", "Studio 2"),
        ("Studio 3", "Studio 3"),
        ("Studio 4", "Studio 4"),
        ("Studio 5", "Studio 5"),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_participants = models.IntegerField(default=10)
    members = models.ManyToManyField('Member', blank=True)

    def __str__(self):
        return self.name
    
    def add_member(self, member):
        if self.members.count() >= self.max_participants:
            raise ValueError("Kelas sudah penuh.")
        if member not in self.members.all():
            self.members.add(member)
