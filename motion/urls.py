from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('personal_trainer/', views.personal_trainer, name='personal_trainer'),
    path('location/', views.location, name='location'),
    path('classes/admin/', views.classes, name='classes'),
    path('about/', views.about, name='about'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/trainer', views.dashboard_trainer, name='dashboard_trainer'),
    path('admin_membership/', views.membership_index, name='membership_index'), # Read
    path('membership/create/', views.membership_create, name='membership_create'),# Create
    path('membership/update/<int:membership_id>/', views.membership_update, name='membership_update'), # Update
    path('membership/delete/<int:membership_id>', views.membership_delete, name='membership_delete'), # Delete
    path('trainer/', views.trainer_index, name='trainer_index'), # Read
    path('trainer/create/', views.trainer_create, name='trainer_create'),# Create
    path('trainer/update/<int:trainer_id>/', views.trainer_update, name='trainer_update'), # Update
    path('trainer/delete/<int:trainer_id>', views.trainer_delete, name='trainer_delete'), # Delete
    path('member/', views.member_index, name='member_index'),
    path('member/create/', views.member_create, name='member_create'),
    path('member/update/<int:member_id>/', views.member_update, name='member_update'),
    path('member/delete/<int:member_id>/', views.member_delete, name='member_delete'),
    path('class/', views.fitness_class_index, name='fitness_class_index'),
    path('class/create/', views.fitness_class_create, name='fitness_class_create'),
    path('class/update/<int:pk>/', views.fitness_class_update, name='fitness_class_update'),
    path('class/delete/<int:pk>/', views.fitness_class_delete, name='fitness_class_delete'),
    path('membership/', views.membership_list, name='membership_list'),
    path('classes/', views.fitnes_class_list, name='fitness_class_list'),
    path('transactions/create/<int:membership_id>/', views.create_transaction, name='create_transaction'),
    path('transactions/confirm/<int:transaction_id>/', views.confirm_transaction, name='confirm_transaction'),
    path('transactions/update/<int:pk>/', views.transaction_update, name='transaction_update'),
    path('transactions/', views.transaction_index, name='transaction_index'),
    ]