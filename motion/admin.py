from django.contrib import admin

# Register your models here.
from motion.models.membership import Membership
from motion.models.trainers import Trainer
from motion.models.members import Member
from motion.models.fitness_class import FitnessClass
from motion.models.transactions import Transaction
from motion.models.additional_class import AdditionalClass

admin.site.register(Membership)
admin.site.register(Trainer)
admin.site.register(Member)
admin.site.register(FitnessClass)
admin.site.register(Transaction)
admin.site.register(AdditionalClass)