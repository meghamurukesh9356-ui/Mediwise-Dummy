from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('update_profile/', views.update_profile, name='update_profile'),
    
    path('logout/', views.logout, name='logout'),
]
