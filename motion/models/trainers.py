from django.db import models

class Trainer(models.Model):
    user = models.OneToOneField('Users', on_delete=models.CASCADE)
    name = models.TextField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.TextField(max_length=50)
    expertise = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
