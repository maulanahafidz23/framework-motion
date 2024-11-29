from django import forms
from .models import Trainer, Membership, Member, FitnessClass, Transaction, AdditionalClass
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import PasswordChangeForm

class MembershipsForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['name', 'limit', 'price', 'duration']

class TrainersForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'email', 'gender', 'expertise']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # Jika update, exclude email dari trainer yang sedang diupdate
            if User.objects.filter(email=email).exclude(email=instance.email).exists():
                raise forms.ValidationError("Email sudah digunakan.")
        else:
            # Jika create baru
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email sudah digunakan.")
        return email
    
class MembersForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'address', 'membership']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['membership'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # Jika update, exclude email dari member yang sedang diupdate
            if User.objects.filter(email=email).exclude(email=instance.email).exists():
                raise forms.ValidationError("Email sudah digunakan.")
        else:
            # Jika create baru
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email sudah digunakan.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Menambahkan validasi untuk nomor telepon (misalnya hanya angka dan panjang maksimal 15 karakter)
        if not phone.isdigit():
            raise forms.ValidationError("Nomor telepon hanya boleh berisi angka.")
        if len(phone) > 15:
            raise forms.ValidationError("Nomor telepon tidak boleh lebih dari 15 karakter.")
        return phone
    
    def save(self, commit=True):
        # Memastikan membership tetap None saat pendaftaran
        member = super().save(commit=False)
        member.membership = None  # Set default membership ke None
        if commit:
            member.save()
        return member
    
    
class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'address']  # Tidak mencantumkan 'membership'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nama Lengkap'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nomor Telepon'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Alamat Lengkap'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Member.objects.filter(email=email).exists():
            raise ValidationError("Email sudah digunakan.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Validasi pola nomor telepon
        if not re.match(r'^\d{10,15}$', phone):
            raise ValidationError("Nomor telepon harus terdiri dari 10-15 angka.")
        return phone

    def save(self, commit=True):
        member = super().save(commit=False)
        member.membership = None  # Membership default adalah None
        if commit:
            member.save()
        return member


class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MemberChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Password Lama",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label="Password Baru",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Konfirmasi Password Baru",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    
class FitnessClassForm(forms.ModelForm):
    trainer = forms.ModelChoiceField(queryset=Trainer.objects.all(), required=True)
    class Meta:
        model = FitnessClass
        fields = ['name', 'trainer', 'schedule', 'price', 'max_participants', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trainer'].queryset = Trainer.objects.all()  # Menampilkan trainer yang ada
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['trainer'].widget.attrs.update({'class': 'form-control'})
        self.fields['schedule'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['max_participants'].widget.attrs.update({'class': 'form-control'})
        
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'proof_of_payment': forms.FileInput(attrs={'class': 'form-control'}),
        }