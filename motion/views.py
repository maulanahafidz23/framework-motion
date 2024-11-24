# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import MembershipsForm, TrainersForm, MembersForm, FitnessClassForm, TransactionForm
from django.contrib.auth.models import User, Group
from .models import Trainer, Membership, Member, FitnessClass, Transaction, AdditionalClass
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Count
from django.views.generic import ListView

# Create your views here.
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

# * DASHBOARD
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
    return render(request, 'dashboard/trainer.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return HttpResponseForbidden("Invalid request method.")


# Autentikasi untuk menu tambahan di Navbar
def your_view(request):
    # Pastikan user sudah login
    if request.user.is_authenticated:
        # Debug: print untuk mengecek group user
        print("User Groups:", request.user.groups.all())
        
        is_member = request.user.groups.filter(name='Member').exists()
        # Debug: print status member
        print("Is Member:", is_member)
    else:
        is_member = False

    context = {
        'is_member': is_member,
    }
    return render(request, 'includes/navbar.html', context)


# READ Membership
def membership_index(request):
    memberships = Membership.objects.all()
    return render(request, 'membership/index.html', {'memberships': memberships})
    
# View untuk halaman Member
def membership_list(request):
    memberships = Membership.objects.all()
    return render(request, 'membership.html', {'memberships': memberships})

#CREATE Membership
def membership_create(request):
    if request.method == 'POST':
        form = MembershipsForm(request.POST)
        if form.is_valid():
            form.save() # Simpan data membership ke database
            messages.success(request, 'Membership berhasil dibuat!') # Pesan sukses
            return redirect('membership_index') # Redirect ke halaman index membership
    else:
        form = MembershipsForm()
    return render(request, 'membership/create.html', {'form': form})

# UPDATE Membership
def membership_update(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    if request.method == 'POST':
        form = MembershipsForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data membership berhasil diubah!')
            return redirect('membership_index')
    else:
        form = MembershipsForm(instance=membership)
    return render(request, 'membership/update.html', {'form': form, 'membership': membership})

# DELETE Membership
def membership_delete(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    membership.delete()
    messages.success(request, 'Data membership berhasil dihapus')
    return JsonResponse({'success': True})



# READ Trainer
def trainer_index(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainer/index.html', {'trainers': trainers})

# CREATE Trainer
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
def trainer_delete(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    trainer.delete()
    messages.success(request, 'Data trainer berhasil dihapus')
    return JsonResponse({'success': True})



# READ Member 
def member_index(request):
    members = Member.objects.all()
    return render(request, 'member/index.html', {'members': members})

# CREATE Member
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
def member_delete(request, member_id):
    membership = get_object_or_404(Member, id=member_id)
    membership.delete()
    messages.success(request, 'Data anggota berhasil dihapus')
    return JsonResponse({'success': True})



# READ Class
def fitness_class_index(request):
    fitness_classes  = FitnessClass.objects.all()  # Mengambil data kelas fitness
    return render(request, 'class/index.html', {'fitness_classes': fitness_classes })

def fitnes_class_list(request):
    fitness_classes = FitnessClass.objects.all()
    return render(request, 'classes.html', {'fitness_classes': fitness_classes})

# CREATE Class
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
def fitness_class_delete(request, pk):
    gymclass = get_object_or_404(FitnessClass, pk=pk)
    gymclass.delete()  
    messages.success(request, 'Kelas berhasil dihapus')
    return JsonResponse({'success': True})


# Transaction Membership

#def create_transaction(request, membership_id):
    # Hanya Member yang bisa melakukan transaksi
    if not hasattr(request.user, 'member'):
        messages.error(request, "Hanya member yang dapat melakukan transaksi.")
        return redirect('membership_list')

    # Dapatkan data membership berdasarkan ID
    membership = get_object_or_404(Membership, id=membership_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.member = request.user.member  # Set member berdasarkan user yang login
            transaction.membership = membership
            transaction.status = 'Pending'  # Default status
            transaction.save()
            messages.success(request, "Transaksi berhasil dibuat! Silakan tunggu konfirmasi pembayaran.")
            return redirect('membership_list')
    else:
        form = TransactionForm()

    return render(request, 'transaction/form.html', {
        'form': form,
        'membership': membership,
    })
   
 
#def create_transaction(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    member = Member.objects.get(email=request.user.email) 

    if request.method == 'POST':
        # Buat transaksi baru
        transaction = Transaction.objects.create(
            member=member,
            membership=membership,
            amount=membership.price,
            status='Pending',
        )
        # Redirect ke halaman konfirmasi untuk mengupload bukti pembayaran
        return redirect('confirm_transaction', transaction_id=transaction.id) 

    # Tampilkan form konfirmasi transaksi
    return render(request, 'transaction/confirm.html', {'membership': membership})    

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
def transaction_index(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction/index.html', {'transactions': transactions})