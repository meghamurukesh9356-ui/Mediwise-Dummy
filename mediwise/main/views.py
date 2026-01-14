from django.shortcuts import render, redirect
from .models import MediAdmin, Patient, Users, Doctor, Pharmacist
from .forms import PatientRegistrationForm, PharmacistRegistrationForm, PatientProfileUpdateForm, DoctorRegistrationForm, PharmacistProfileUpdateForm
from django.contrib import messages



# Create your views here.

def index(request):
    return render(request, 'index.html')

def getUser(email, password): # Import here to avoid circular import
    mapping = {
        'admin': MediAdmin,
        'patient': Patient,
        'pharmacist': Pharmacist,
        'doctor': Doctor
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
            request.session['admin_id'] = user_obj.id
            return redirect('admin_dashboard')
        elif role == 'patient':
            request.session['patient_id'] = user_obj.id
            return redirect('patient_dashboard')
        elif role == 'pharmacist':
            request.session['pharmacist_id'] = user_obj.id
            return redirect('pharmacist_dashboard')
        elif role == 'doctor':
            request.session['doctor_id'] = user_obj.id
            return redirect('doctor_dashboard')
        
        return render(request, 'login.html', {'error': 'Invalid credentials'})
        
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('index')

def admin_dashboard(request):
    # Check if admin is logged in
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')
    
    try:
        admin = MediAdmin.objects.get(id=admin_id)
    except MediAdmin.DoesNotExist:
        return redirect('login')
    
    return render(request, 'admin/dashboard.html', {'admin': admin})

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


def admin_profile(request):
    admin_id = request.session.get('admin_id')
    
    if not admin_id:
        return redirect('login')
    
    try:
        admin = MediAdmin.objects.get(id=admin_id)
    except MediAdmin.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        admin.email = request.POST.get('email')
        admin.password = request.POST.get('password')
        admin.save()
        messages.success(request, "Admin profile updated successfully!")
        return redirect('admin_profile')
    else:
        context = {
            'admin': admin
        }
    return render(request, 'admin/profile.html', context)


def pharmacist_dashboard(request):
    from .models import Pharmacist  # Import here to avoid circular import
    
    pharmacist_id = request.session.get('pharmacist_id')
    
    if not pharmacist_id:
        return redirect('login')
    
    try:
        pharmacist = Pharmacist.objects.get(id=pharmacist_id)
    except:
        return redirect('login')
    
    # Dummy data for dashboard
    dashboard_data = {
        'prescriptions_pending': 12,
        'medications_low_stock': 5,
        'today_orders': 24,
        'weekly_sales': 12500,
        'recent_customers': [
            {'name': 'John Doe', 'contact': 'john@example.com', 'last_visit': 'Today'},
            {'name': 'Jane Smith', 'contact': 'jane@example.com', 'last_visit': 'Yesterday'},
            {'name': 'Robert Johnson', 'contact': 'robert@example.com', 'last_visit': '2 days ago'},
        ],
        'low_stock_medications': [
            {'name': 'Aspirin', 'quantity': 5},
            {'name': 'Amoxicillin', 'quantity': 3},
            {'name': 'Lisinopril', 'quantity': 7},
            {'name': 'Metformin', 'quantity': 2},
            {'name': 'Atorvastatin', 'quantity': 4},
        ]
    }
    
    context = {
        'pharmacist': pharmacist,
        'data': dashboard_data
    }
    return render(request, 'pharmacist/dashboard.html', context)


def pharmacist_profile(request):
    
    pharmacist_id = request.session.get('pharmacist_id')
    
    if not pharmacist_id:
        return redirect('login')
    
    try:
        pharmacist = Pharmacist.objects.get(id=pharmacist_id)
    except:
        return redirect('login')
    
    if request.method == 'POST':
        form = PharmacistProfileUpdateForm(request.POST, instance=pharmacist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('pharmacist_profile')
    else:
        form = PharmacistProfileUpdateForm(instance=pharmacist)
    
    # Pass password value for display as dots
    context = {
        'pharmacist': pharmacist,
        'form': form,
        'has_password': bool(pharmacist.password and pharmacist.password.strip()),
        'current_password': pharmacist.password if pharmacist.password else ''
    }
    return render(request, 'pharmacist/profile.html', context)

def doctor_dashboard(request):
    user_id = request.session.get('doctor_id')
    if not user_id:
        return redirect('login')
    
    try:
        doctor = Doctor.objects.get(id=user_id)
    except Doctor.DoesNotExist:
        return redirect('login')
    
    # Check profile completion (customize as needed)
    required_fields = [doctor.description, doctor.profile_picture, doctor.cureentHospital, doctor.license_number, doctor.address]
    profile_incomplete = any(field in [None, '', 'None'] for field in required_fields)

    context = {
        'user': doctor,
        'profile_incomplete': profile_incomplete,
    }
    return render(request, 'doctor/dashboard.html', context)

def doctor_profile(request):
    user_id = request.session.get('doctor_id')
    if not user_id:
        return redirect('login')
    
    try:
        doctor = Doctor.objects.get(id=user_id)
    except Doctor.DoesNotExist:
        return redirect('login')
    
    from .forms import DoctorProfileUpdateForm
    
    if request.method == 'POST':
        print(f"POST data keys: {list(request.POST.keys())}")
        print(f"FILES data keys: {list(request.FILES.keys())}")
        
        form = DoctorProfileUpdateForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            saved_doctor = form.save()
            return redirect('doctor_profile')
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, "Please correct the errors below.")
    else:
        form = DoctorProfileUpdateForm(instance=doctor)
    
    # Pass password value for display as dots and profile picture status
    context = {
        'form': form, 
        'user': doctor,
        'has_password': bool(doctor.password and doctor.password.strip()),
        'current_password': doctor.password if doctor.password else '',
        'has_profile_picture': bool(doctor.profile_picture)
    }
    return render(request, 'doctor/profile.html', context)

def register(request):
    # Initialize empty forms for a GET request
    patient_form = PatientRegistrationForm()
    pharmacist_form = PharmacistRegistrationForm()
    registered = False
    
    if request.method == 'POST':
        role = request.POST.get('role')
        
        if role == 'patient':
            patient_form = PatientRegistrationForm(request.POST)
            if patient_form.is_valid():
                user_role = Users.objects.create(role='patient')
                patient = patient_form.save(commit=False)
                patient.user = user_role
                patient.save()
                registered = True
            # If invalid, patient_form now contains error data
                
        elif role == 'pharmacist':
            pharmacist_form = PharmacistRegistrationForm(request.POST)
            if pharmacist_form.is_valid():
                user_role = Users.objects.create(role='pharmacist')
                pharmacist = pharmacist_form.save(commit=False)
                pharmacist.user = user_role
                pharmacist.save()
                registered = True
            # If invalid, pharmacist_form now contains error data

    # This context now contains the forms with their respective errors
    context = {
        'patient_form': patient_form,
        'pharmacist_form': pharmacist_form,
        'registered': registered
    }
    return render(request, 'register.html', context)

def manage_doctors(request):
    # Ensure admin authentication
    if not request.session.get('admin_id'):
        return redirect('login')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            form = DoctorRegistrationForm(request.POST)
            if form.is_valid():
                # Create base User entry first (if your logic requires it for doctors too)
                # Assuming Doctors also need a Users entry like Patients/Pharmacists
                user_role = Users.objects.create(role='doctor')
                
                doctor = form.save(commit=False)
                doctor.user = user_role
                doctor.save()
                messages.success(request, "Doctor added successfully!")
            else:
                messages.error(request, "Error adding doctor. Please check the form.")
                
        elif action == 'edit':
            doctor_id = request.POST.get('doctor_id')
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                form = DoctorRegistrationForm(request.POST, instance=doctor)
                # Password is optional in edit if left blank, but form might require it. 
                # For simplicity here, we assume full update or handled by form logic.
                if form.is_valid():
                    form.save()
                    messages.success(request, "Doctor updated successfully!")
                else:
                    messages.error(request, "Error updating doctor.")
            except Doctor.DoesNotExist:
                messages.error(request, "Doctor not found.")
                
        elif action == 'delete':
            doctor_id = request.POST.get('doctor_id')
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                if doctor.user:
                    doctor.user.delete() # Cascade should handle doctor deletion usually, or delete both
                else:
                    doctor.delete()
                messages.success(request, "Doctor deleted successfully!")
            except Doctor.DoesNotExist:
                messages.error(request, "Doctor not found.")
                
        return redirect('manage_doctors')
        
    # GET request
    doctors = Doctor.objects.all().order_by('-registration_date')
    form = DoctorRegistrationForm()
    
    return render(request, 'admin/doctors.html', {
        'doctors': doctors,
        'form': form
    })
