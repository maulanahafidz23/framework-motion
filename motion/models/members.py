from django.db import models
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    membership = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True, blank=True)
    classes_taken = models.IntegerField(default=0) # untuk menyimpan data kelas yang telah diambil perminggu

    def __str__(self):
        return self.name
    
    def can_take_class(self):
        if self.membership:
            # Periksa jika member sudah mencapai batas kelas
            return self.classes_taken < self.membership.max_classes_per_week
        return True  # Member tanpa membership bisa ikut kelas tambahan
        
# Signal to create a User when a Member is created
@receiver(post_save, sender=Member)
def create_user_for_member(sender, instance, created, **kwargs):
    if created:
        # Cek jika email sudah digunakan
        if User.objects.filter(email=instance.email).exists():
            raise ValidationError(f"Email {instance.email} sudah terdaftar!")
        
        # Create the corresponding User
        user = User.objects.create_user(
            username=instance.email,  # Use email as username
            email=instance.email
        )
        
        # Use the member's name as the password
        user.set_password(instance.name)  # Set password using the member's name
        user.save()

        # Add user to the 'Member' group
        member_group, _ = Group.objects.get_or_create(name='Member')
        user.groups.add(member_group)