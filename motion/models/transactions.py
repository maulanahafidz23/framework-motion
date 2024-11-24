from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Transaction(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    membership = models.ForeignKey('Membership', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])
    proof_of_payment = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction {self.id} - {self.status}"


@receiver(post_save, sender=Transaction)
def update_membership(sender, instance, **kwargs):
    if instance.status == 'Paid':
        # Perbarui membership member
        member = instance.member
        member.membership = instance.membership
        member.save()