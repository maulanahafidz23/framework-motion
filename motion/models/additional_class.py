from django.db import models

class AdditionalClass(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    fit_class = models.ForeignKey('FitnessClass', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    proof_of_payment = models.ImageField(upload_to='additional_class/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member.name} - {self.fit_class.name} - {self.status}"