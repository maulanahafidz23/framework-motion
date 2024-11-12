from django.db import models

class Member(models.Model):
    user = models.OneToOneField('Users', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    membership = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True, blank=True)
    classes_taken = models.IntegerField(default=0) # untuk menyimpan data kelas yang telah diambil perminggu

    def __str__(self):
        return self.user.username
