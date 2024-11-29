
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Halaman utama
    path('', views.home, name='home'),

    # Halaman publik
    path('membership/', views.membership_list, name='membership_list'),
    path('personal_trainer/', views.personal_trainer, name='personal_trainer'),
    path('location/', views.location, name='location'),
    path('classes/', views.fitnes_class_list, name='fitness_class_list'),
    path('about/', views.about, name='about'),

    # Halaman autentikasi
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_member, name='register_member'),

    # Halaman dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/trainer', views.dashboard_trainer, name='dashboard_trainer'),

    # CRUD Membership
    path('admin_membership/', views.membership_index, name='membership_index'),  # Read
    path('membership/create/', views.membership_create, name='membership_create'),  # Create
    path('membership/update/<int:membership_id>/', views.membership_update, name='membership_update'),  # Update
    path('membership/delete/<int:membership_id>', views.membership_delete, name='membership_delete'),  # Delete

    # CRUD Trainer
    path('trainer/', views.trainer_index, name='trainer_index'),  # Read
    path('trainer/create/', views.trainer_create, name='trainer_create'),  # Create
    path('trainer/update/<int:trainer_id>/', views.trainer_update, name='trainer_update'),  # Update
    path('trainer/delete/<int:trainer_id>/', views.trainer_delete, name='trainer_delete'),  # Delete

    # CRUD Member
    path('member/', views.member_index, name='member_index'),
    path('member/create/', views.member_create, name='member_create'),
    path('member/update/<int:member_id>/', views.member_update, name='member_update'),
    path('member/delete/<int:member_id>/', views.member_delete, name='member_delete'),

    # CRUD Fitness Class
    path('class/', views.fitness_class_index, name='fitness_class_index'),
    path('class/create/', views.fitness_class_create, name='fitness_class_create'),
    path('class/update/<int:pk>/', views.fitness_class_update, name='fitness_class_update'),
    path('class/delete/<int:pk>/', views.fitness_class_delete, name='fitness_class_delete'),
    
    # Pendaftaran kelas oleh member
    path('join-class/<int:class_id>/', views.join_class, name='join_class'),
    
    # Menampilkan Kelas untuk Trainer
    path('trainer/classes/', views.trainer_classes, name='trainer_classes'),
    
    # Menampilkan Kelas untuk Member
    path('member/classes/', views.member_classes, name='member_classes'),
    

    # Transaksi
    path('transactions/create/<int:membership_id>/', views.create_transaction, name='create_transaction'),
    path('transactions/confirm/<int:transaction_id>/', views.confirm_transaction, name='confirm_transaction'),
    path('transactions/update/<int:pk>/', views.transaction_update, name='transaction_update'),
    path('transactions/', views.transaction_index, name='transaction_index'),
    path('transactions/update_additional_class/<int:additional_class_id>/', views.update_additional_class, name='update_additional_class'),
    
    # Menampilkan Riwayat Transaksi
    path('transactions/history/', views.transaction_history, name='transaction_history'),
    
    # Halaman pembayaran tambahan jika member melewati batas kelas atau tidak memiliki membership
    path('transactions/transaction_additional_class/<int:class_id>/', views.transaction_additional_class, name='transaction_additional_class'),
    
    # Profile
    path('profile/trainer', views.profile_trainer, name='profile_trainer'),
    path('profile/member', views.profile_member, name='profile_member'),
    path('profile/edit/<int:member_id>/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
