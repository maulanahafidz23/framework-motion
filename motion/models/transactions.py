from django.db import models

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
