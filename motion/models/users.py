from django.db import models

class Users(models.Model):
    ADMIN = 1
    TRAINER = 2
    MEMBER = 3
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (TRAINER, 'Trainer'),
        (MEMBER, 'Member')
    )

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) # Panjang standar untuk password hash di Django
    role = models.IntegerField(choices=ROLE_CHOICES) 

def __str__(self):
    return self.username