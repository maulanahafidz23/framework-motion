from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

class Trainer(models.Model):
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    name = models.TextField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    expertise = models.CharField(max_length=100)

    def __str__(self):
        return self.name

        
    # Signal to create a User when a Trainer is created
@receiver(post_save, sender=Trainer)
def create_user_for_trainer(sender, instance, created, **kwargs):
    if created:
        # Cek jika email sudah digunakan
        if User.objects.filter(email=instance.email).exists():
            raise ValidationError(f"Email {instance.email} sudah terdaftar!")
        
        # Create the corresponding User
        user = User.objects.create_user(
            username=instance.email,  # Use email as username
            email=instance.email
        )
        
        # Use the trainer's name as the password
        user.set_password(instance.name)  # Set password using the trainer's name
        user.save()

        # Add user to the 'Trainer' group
        trainer_group, _ = Group.objects.get_or_create(name='Trainer')
        user.groups.add(trainer_group)