from django.shortcuts import render, redirect
from .models import MediAdmin, Patient, Users
from .forms import PatientRegistrationForm, PharmacistRegistrationForm, PatientProfileUpdateForm
from django.contrib import messages



# Create your views here.

def index(request):
    return render(request, 'index.html')

def getUser(email, password):
    mapping = {
        'admin': MediAdmin,
        'patient': Patient
    }

    for role, model in mapping.items():
        user = model.objects.filter(email=email, password=password).first()
        if user:
            return role, user # Return the object too so you can use it
    return None, None

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        role, user_obj = getUser(email, password)
        
        if role == 'admin':
            return redirect('admin_dashboard')
        elif role == 'patient':
            request.session['patient_id'] = user_obj.id
            return redirect('patient_dashboard')
        
        return render(request, 'login.html', {'error': 'Invalid credentials'})
        
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('index')

def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

def patient_dashboard(request):
    user_id = request.session.get('patient_id')
    if user_id is None:
        return redirect('login')
    
    user = Patient.objects.filter(id=user_id).first()
    
    # Define which fields are required for a "complete" profile
    # Add or remove fields based on your Patient model
    required_fields = [user.phone_number, user.address, user.date_of_birth, user.blood_group, user.height, user.weight]
    profile_incomplete = any(field in [None, '', 'None'] for field in required_fields)

    context = {
        'user': user,
        'profile_incomplete': profile_incomplete,
    }
    return render(request, 'patient/dashboard.html', context)

def update_profile(request):
    user_id = request.session.get('patient_id')
    if not user_id:
        return redirect('login')
    
    try:
        patient = Patient.objects.get(id=user_id)
    except Patient.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        # instance=patient populates the form with existing data and maps the POST data to it
        form = PatientProfileUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully! Redirecting...")
    else:
        # This automatically pre-fills the fields with current data
        form = PatientProfileUpdateForm(instance=patient)
    
    return render(request, 'patient/profile.html', {
        'form': form, 
        'user': patient
    })


def register(request):
    patient_form = PatientRegistrationForm()
    pharmacist_form = PharmacistRegistrationForm()
    
    if request.method == 'POST':
        role = request.POST.get('role')
        print(role)
        
        if role == 'patient':
            patient_form = PatientRegistrationForm(request.POST)
            if patient_form.is_valid():
                # Create the Users instance first
                user_role = Users.objects.create(role='patient')
                
                # Save the patient
                patient = patient_form.save(commit=False)
                patient.user = user_role
                patient.save()
                
                return redirect('login')
        
        elif role == 'pharmacist':
            pharmacist_form = PharmacistRegistrationForm(request.POST)
            if pharmacist_form.is_valid():
                # Create the Users instance first
                user_role = Users(role='pharmacist')
                user_role.save()
                
                # Save the pharmacist
                pharmacist = pharmacist_form.save(commit=False)
                pharmacist.user = user_role
                pharmacist.save()
                
                return redirect('login')
        else:
            print(patient_form.errors)
            print(pharmacist_form.errors)
    
    context = {
        'patient_form': patient_form,
        'pharmacist_form': pharmacist_form,
    }
    return render(request, 'register.html', context)
