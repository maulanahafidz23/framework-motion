# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
import requests
from .forms import MemberChangePasswordForm, MembershipsForm, TrainerChangePasswordForm, TrainerUpdateForm, TrainersForm, MembersForm, FitnessClassForm, TransactionForm, MemberRegistrationForm, MemberUpdateForm
from .models import Trainer, Membership, Member, FitnessClass, Transaction, AdditionalClass
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
import os
from .decorators import admin_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MembershipSerializer


### ---   PUBLIK   --- ###

def home(request):
    return render(request, 'home.html')

def membership(request):
    return render(request, 'membership.html')

def personal_trainer(request):
    return render(request, 'personal_trainer.html')

def location(request):
    return render(request, 'location.html')

def classes(request):
    return render(request, 'classes.html')

def about(request):
    return render(request, 'about.html')

def fitnes_class_list(request):
    fitness_classes = FitnessClass.objects.all()
    return render(request, 'classes.html', {'fitness_classes': fitness_classes})

def register_member(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registrasi berhasil! Silakan login.")
            return redirect('login')  # Ganti dengan URL halaman login Anda
        else:
            messages.error(request, "Ada kesalahan dalam pengisian form.")
    else:
        form = MemberRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def membership_list(request):
    memberships = Membership.objects.all()
    return render(request, 'membership.html', {'memberships': memberships})



### ---   DASHBOARD   --- ###

@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif user.groups.filter(name='Trainer').exists():
        return redirect('dashboard_trainer')
    elif user.groups.filter(name='Member').exists():
        return redirect('home')  # Arahkan ke tampilan awal website
    return HttpResponseForbidden("You do not have permission to access this page.")

@login_required
def dashboard_admin(request):
    return render(request, 'dashboard/admin/admin.html')

@login_required
def dashboard_trainer(request):
    return render(request, 'dashboard/trainer/trainer.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return HttpResponseForbidden("Invalid request method.")
    
    
### ---   TRAINER   --- ###
        
@login_required
def profile_trainer(request):
    try:
        trainer = Trainer.objects.get(email=request.user.email)
        form = TrainerUpdateForm(instance=trainer)
    except Trainer.DoesNotExist:
        trainer = None

    return render(request, 'dashboard/trainer/profile.html', {'trainer': trainer, 'profile_form': form})

@login_required
def edit_profile_trainer(request, trainer_id):
    try:
        trainer = Trainer.objects.get(id=trainer_id)
        if request.method == 'POST':
            form = TrainerUpdateForm(request.POST, instance=trainer)
            print("Data POST diterima:", request.POST)  # Debug data POST
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                print("Error pada form:", form.errors.as_json())  # Log error form
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Trainer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Trainer not found'})

    
@login_required
def change_password_trainer(request):
    if request.method == 'POST':
        form_password = TrainerChangePasswordForm(user=request.user, data=request.POST)
        if form_password.is_valid():
            form_password.save()  
            update_session_auth_hash(request, form_password.user)
            return JsonResponse({'success': True})
        else:
            error_messages = []
            for field, errors in form_password.errors.items():
                for error in errors:
                    error_messages.append(error)  
            error_message = " ".join(error_messages)  
            return JsonResponse({'success': False, 'error': error_message})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def trainer_classes(request):
    # Pastikan user adalah trainer
    try:
        trainer = Trainer.objects.get(email=request.user.email)
    except Trainer.DoesNotExist:
        return render(request, 'error.html', {'message': 'Anda bukan trainer.'})

    # Ambil semua kelas
    all_classes = FitnessClass.objects.all()

    # Ambil kelas yang dia ajar
    my_classes = FitnessClass.objects.filter(trainer=trainer)

    return render(request, 'dashboard/trainer/classes.html', {
        'all_classes': all_classes,
        'my_classes': my_classes,
    })




### ---   MEMBER   --- ###

@login_required
def profile_member(request):
    try:
        member = Member.objects.get(email=request.user.email) 
        form = MemberUpdateForm(instance=member)
        form_password = MemberChangePasswordForm(user=request.user)
    except Member.DoesNotExist:
        member = None

    return render(request, 'profile.html', {
        'member': member, 
        'profile_form': form, 
        'password_form' : form_password})

@login_required
def edit_profile(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
        if request.method == 'POST':
            form = MemberUpdateForm(request.POST, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profil berhasil diperbarui')
                return JsonResponse({'success': True})  
        return JsonResponse({'success': False, 'error': 'Invalid form submission'})
    except Member.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Member not found'})
    
@login_required
def change_password(request):
    if request.method == 'POST':
        form_password = MemberChangePasswordForm(user=request.user, data=request.POST)
        if form_password.is_valid():
            form_password.save()  
            update_session_auth_hash(request, form_password.user)
            return JsonResponse({'success': True})
        else:
            error_messages = []
            for field, errors in form_password.errors.items():
                for error in errors:
                    error_messages.append(error)  
            error_message = " ".join(error_messages)  
            return JsonResponse({'success': False, 'error': error_message})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def create_transaction(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    member = Member.objects.get(email=request.user.email)  # Mendapatkan data member dari user

    if request.method == 'POST':
        # Buat transaksi baru
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.member = member
            transaction.membership = membership
            transaction.amount = membership.price
            transaction.status = 'Pending'
            transaction.save()
            return redirect('confirm_transaction', transaction_id=transaction.id)
    else:
        form = TransactionForm(initial={
            'amount': membership.price,
        })

    return render(request, 'transaction/form.html', {
        'form': form,
        'membership': membership,
        'member': member,  # Kirim data member ke template
    })
    
@login_required
def join_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    try:
        member = Member.objects.get(email=request.user.email)    
    except Member.DoesNotExist:
        messages.error(request, "Anda belum terdaftar sebagai Member.")
        return redirect('fitness_class_list')

    # Periksa apakah kelas penuh
    if fitness_class.members.count() >= fitness_class.max_participants:
        messages.error(request, "Kelas sudah penuh.")
        return redirect('fitness_class_list')

    # Cek apakah member bisa mengambil kelas
    if member.can_take_class():
        # Tambahkan ke kelas karena masih dalam limit membership
        fitness_class.add_member(member)
        member.classes_taken += 1
        member.save()
        messages.success(request, f"Anda berhasil bergabung dengan kelas {fitness_class.name}.")
        return redirect('fitness_class_list')
    else:
        # Arahkan ke pembayaran jika sudah mencapai limit atau tidak punya membership
        return redirect('transaction_additional_class', class_id=class_id)
    
@login_required
def transaction_additional_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    
    try:
        member = Member.objects.get(email=request.user.email)
    except Member.DoesNotExist:
        messages.error(request, "Anda belum terdaftar sebagai Member.")
        return redirect('fitness_class_list')

    if request.method == 'POST':
        if 'payment_proof' not in request.FILES:
            messages.error(request, "Mohon upload bukti pembayaran.")
            return render(request, 'transaction/form_class.html', {
                'fitness_class': fitness_class
            })

        payment_proof = request.FILES['payment_proof']
        
        # Validasi file
        try:
            validate_payment_proof(payment_proof)
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'transaction/form_class.html', {
                'fitness_class': fitness_class
            })

        try:
            # Buat transaksi tambahan untuk kelas
            additional_class = AdditionalClass.objects.create(
                member=member,
                fit_class=fitness_class,
                price=fitness_class.price,
                proof_of_payment=payment_proof,  # ImageField akan otomatis handle upload
                status='Pending'
            )
            
            messages.success(request, "Transaksi berhasil dibuat. Silakan tunggu verifikasi dari admin.")
            return redirect('transaction_history')
            
        except Exception as e:
            # Jika terjadi error saat menyimpan, hapus file yang sudah terupload
            if payment_proof:
                try:
                    default_storage.delete(payment_proof.name)
                except:
                    pass
            messages.error(request, "Terjadi kesalahan saat membuat transaksi. Silakan coba lagi.")
            return render(request, 'transaction/form_class.html', {
                'fitness_class': fitness_class
            })

    return render(request, 'transaction/form_class.html', {
        'fitness_class': fitness_class
    })
    
@login_required
def confirm_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == 'POST':
        # Upload bukti pembayaran
        if 'proof_of_payment' in request.FILES:
            transaction.proof_of_payment = request.FILES.get('proof_of_payment')
            transaction.status = 'Pending'  # Status tetap Pending hingga diverifikasi oleh admin
            transaction.save()
            messages.success(request, 'Bukti pembayaran berhasil diupload')
        else:
            messages.error(request, 'Harap pilih file bukti pembayaran')
            
        return redirect('membership_list')
    
    return render(request, 'transaction/confirm.html', {'transaction': transaction})

@login_required
def member_classes(request):
    # Ambil data member berdasarkan ID
    member = Member.objects.get(email=request.user.email)
    
    # Ambil kelas yang diikuti member
    classes = member.fitnessclass_set.all()  # Karena ManyToManyField

    context = {
        'member': member,
        'classes': classes,
    }
    return render(request, 'member_classes.html', context)

@login_required
def transaction_history(request):
    try:
        # Mendapatkan data member dari user yang sedang login
        member = Member.objects.get(email=request.user.email)
    except Member.DoesNotExist:
        messages.error(request, "Anda belum terdaftar sebagai Member.")
        return redirect('profile_member')

    # Ambil semua transaksi membership dan tambahan kelas yang terkait dengan member ini
    membership_transactions = Transaction.objects.filter(member=member).order_by('-create_date')
    additional_class_transactions = AdditionalClass.objects.filter(member=member).order_by('-date')

    context = {
        'membership_transactions': membership_transactions,
        'additional_class_transactions': additional_class_transactions,
        'member': member,
    }

    return render(request, 'transaction/history.html', context)





### ---   ADMIN   --- ###




# READ Trainer
@admin_required
def trainer_index(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainer/index.html', {'trainers': trainers})

# CREATE Trainer
@admin_required
def trainer_create(request):
    if request.method == 'POST':
        form = TrainersForm(request.POST)
        if form.is_valid():
            form.save()  # Simpan data trainer ke database
            messages.success(request, 'Trainer berhasil dibuat!')  # Pesan sukses
            return redirect('trainer_index')  # Redirect ke halaman index trainer
        else:
            messages.error(request, 'Ada kesalahan dalam pengisian form.')
    else:
        form = TrainersForm()
    return render(request, 'trainer/create.html', {'form': form})

# UPDATE Trainer
@admin_required
def trainer_update(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    
    if request.method == 'POST':
        form = TrainersForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Pelatih berhasil diubah!')
            return redirect('trainer_index')  # Redirect setelah berhasil
    else:
        form = TrainersForm(instance=trainer)  # Form untuk method GET
    
    return render(request, 'trainer/update.html', {'form': form, 'trainer': trainer})
        
# DELETE Trainer
@admin_required
def trainer_delete(request, trainer_id):
    if request.method == 'POST':
        trainer = get_object_or_404(Trainer, id=trainer_id)
        trainer.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# READ Member 
@admin_required
def member_index(request):
    members = Member.objects.all()
    return render(request, 'member/index.html', {'members': members})

# CREATE Member
@admin_required
def member_create(request):
    if request.method == 'POST':
        form = MembersForm(request.POST)
        if form.is_valid():
            form.save()  # Simpan data member ke database
            messages.success(request, 'Member berhasil dibuat!')  # Pesan sukses
            return redirect('member_index')  # Redirect ke halaman index Member
        else:
            messages.error(request, 'Ada kesalahan dalam pengisian form.')
    else:
        form = MembersForm()
    return render(request, 'member/create.html', {'form': form})

# UPDATE Member
@admin_required
def member_update(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = MembersForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member berhasil diperbarui!')
            return redirect('member_index')
    else:
        form = MembersForm(instance=member)

    return render(request, 'member/update.html', {'form': form, 'member': member})

# DELETE Member
@admin_required
def member_delete(request, member_id):
    membership = get_object_or_404(Member, id=member_id)
    membership.delete()
    messages.success(request, 'Data anggota berhasil dihapus')
    return JsonResponse({'success': True})


# READ Class
@admin_required
def fitness_class_index(request):
    fitness_classes  = FitnessClass.objects.all()  # Mengambil data kelas fitness
    return render(request, 'class/index.html', {'fitness_classes': fitness_classes })

# CREATE Class
@admin_required
def fitness_class_create(request):
    if request.method == 'POST':
        form = FitnessClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kelas berhasil dibuat!')
            return redirect('fitness_class_index')
        else:
            messages.error(request, 'Ada kesalahan dalam form, silakan periksa kembali.')
    else:
        form = FitnessClassForm()
    return render(request, 'class/create.html', {'form': form})

# UPDATE GymClass
@admin_required
def fitness_class_update(request, pk):
    fitness_class = get_object_or_404(FitnessClass, pk=pk)
    if request.method == 'POST':
        form = FitnessClassForm(request.POST, instance=fitness_class)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kelas fitness berhasil diupdate!')
            return redirect('fitness_class_index')
        else:
            messages.error(request, 'Ada kesalahan dalam form, silakan periksa kembali.')
    else:
        form = FitnessClassForm(instance=fitness_class)
    return render(request, 'class/update.html', {'form': form})

# DELETE GymClass
@admin_required
def fitness_class_delete(request, pk):
    gymclass = get_object_or_404(FitnessClass, pk=pk)
    gymclass.delete()  
    messages.success(request, 'Kelas berhasil dihapus')
    return JsonResponse({'success': True})


# UPDATE Transaction
@admin_required
def update_additional_class(request, additional_class_id):
    # Ambil data AdditionalClass berdasarkan ID
    additional_class = get_object_or_404(AdditionalClass, id=additional_class_id)
    
    if request.method == 'POST':
        # Ambil status dari form
        new_status = request.POST.get('status')
        
        # Update status transaksi
        additional_class.status = new_status
        
        # Jika status menjadi "Paid", tambahkan member ke kelas dan perbarui informasi terkait
        if new_status == 'Paid':
            # Tambahkan member ke kelas
            additional_class.fit_class.add_member(additional_class.member)
            additional_class.member.classes_taken += 1
            additional_class.member.save()
            messages.success(request, "Pembayaran berhasil diverifikasi, dan member telah ditambahkan ke kelas.")
        else:
            messages.success(request, f"Status transaksi berhasil diubah menjadi {new_status}.")
        
        # Simpan perubahan pada transaksi
        additional_class.save()
        return redirect('transaction_index')
    
    # Dapatkan URL gambar bukti pembayaran jika tersedia
    proof_image_url = additional_class.proof_of_payment.url if additional_class.proof_of_payment else None
    
    return render(request, 'transaction/update_additional.html', {
        'additional_class': additional_class,
        'proof_image_url': proof_image_url
    })

# UPDATE Transaction
@admin_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    
    if request.method == 'POST':
        # Ambil data dari form
        status = request.POST.get('status')
        
        # Update status transaksi
        transaction.status = status
        transaction.save()
        
        messages.success(request, 'Status transaksi berhasil diperbarui')
        return redirect('transaction_index')
    
    # Dapatkan URL gambar bukti pembayaran jika ada
    proof_image_url = transaction.proof_of_payment.url if transaction.proof_of_payment else None
    
    return render(request, 'transaction/update.html', {
        'transaction': transaction,
        'proof_image_url': proof_image_url
    })

# READ Transaction 
@admin_required
def transaction_index(request):
    transactions = Transaction.objects.all()
    additional_classes = AdditionalClass.objects.all()
    return render(request, 'transaction/index.html', {
        'transactions': transactions,
        'additional_classes': additional_classes,
    })

def is_admin(user):
    return user.is_staff or user.is_superuser


    
### ---   VALIDASI   --- ### 
   
def validate_payment_proof(file):
    # Validasi ukuran file (maksimal 2MB)
    max_size = 2 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError('Ukuran file terlalu besar. Maksimal ukuran file adalah 2MB.')
    
    # Validasi tipe file
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
    if file.content_type not in allowed_types:
        raise ValidationError('Format file tidak didukung. Gunakan JPG atau PNG.')
    
    # Validasi nama file
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Format file tidak didukung. Gunakan JPG atau PNG.')
    
    # Validasi dimensi gambar (opsional)
    try:
        from PIL import Image
        img = Image.open(file)
        max_dimension = 2000  # maksimal 2000x2000 pixels
        if img.width > max_dimension or img.height > max_dimension:
            raise ValidationError(
                f'Dimensi gambar terlalu besar. Maksimal dimensi adalah {max_dimension}x{max_dimension} pixels.'
            )
    except:
        # Jika gagal memvalidasi dimensi, lewati
        pass
    
    
    
    
from rest_framework import viewsets
from .serializers import MembershipSerializer
...
# API
class MembershipViewSet(viewsets.ModelViewSet):
    """
    API endpoint yang memungkinkan operasi CRUD untuk model Membership.
    """
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer # Menggunakan serializer yang sudah kita buat
    

# CREATE Membership
def membership_create(request):
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'price': request.POST.get('price'),
            'duration': request.POST.get('duration'),  # Misalnya durasi dalam hari/bulan
            'limit': request.POST.get('limit')  # Ambil data limit
        }
        response = requests.post('http://127.0.0.1:8000/api/memberships/', data=form_data)
        if response.status_code == 201:
            messages.success(request, 'Membership berhasil dibuat!')
            return redirect('membership_index')
        else:
            messages.error(request, f'Gagal membuat membership: {response.text}')
    else:
        form_data = {}

    return render(request, 'membership/create.html', {'form': MembershipsForm()})



# READ Membership
def membership_index(request):
    # Mengirim GET request untuk mengambil semua data membership
    response = requests.get('http://127.0.0.1:8000/api/memberships/')

    if response.status_code == 200:
        memberships = response.json()  # Ambil data membership dalam format JSON
    else:
        memberships = []  # Jika gagal, siapkan list kosong

    return render(request, 'membership/index.html', {'memberships': memberships})



def membership_update(request, membership_id):
    if request.method == 'POST':
        # Mengambil data dari form
        form_data = {
            'name': request.POST.get('name'),
            'price': request.POST.get('price'),
            'duration': request.POST.get('duration'),  # Durasi dalam hari
            'limit': request.POST.get('limit'),
        }
        # Mengirim PUT request ke API
        response = requests.put(
            f'http://127.0.0.1:8000/api/memberships/{membership_id}/',
            data=form_data
        )
        if response.status_code == 200:  # Jika berhasil
            messages.success(request, 'Data membership berhasil diubah!')
            return redirect('membership_index')  # Redirect ke halaman index membership
        else:
            messages.error(request, f'Gagal mengubah membership: {response.text}')
    else:
        # Mendapatkan data membership saat ini dari API
        response = requests.get(f'http://127.0.0.1:8000/api/memberships/{membership_id}/')
        if response.status_code == 200:
            membership = response.json()  # Ambil data membership dalam format JSON
        else:
            return HttpResponseForbidden("Data membership tidak ditemukan.")

    # Render halaman dengan form berisi data awal
    return render(request, 'membership/update.html', {
        'form': MembershipsForm(initial=membership), 
        'membership': membership
    })


def membership_delete(request, membership_id):
    if request.method == 'POST':  # Hanya menerima metode POST untuk menghapus
        # Mengirim DELETE request ke API
        response = requests.delete(f'http://127.0.0.1:8000/api/memberships/{membership_id}/')
        if response.status_code == 204:  # No Content, berarti berhasil dihapus
            messages.success(request, 'Data membership berhasil dihapus')
            return JsonResponse({'success': True})
        else:
            messages.error(request, f'Gagal menghapus membership: {response.text}')
            return JsonResponse({'success': False})
    else:
        return HttpResponseForbidden("Metode tidak diizinkan.")
