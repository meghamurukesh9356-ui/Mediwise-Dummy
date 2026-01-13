from django import forms
from . models import Patient, Pharmacist

class PatientRegistrationForm(forms.ModelForm):
    """
    Form for initial patient registration with essential fields
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your last name'
        })
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Create a secure password'
        }),
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your email address'
        })
    )

    class Meta:
        model = Patient
        fields = ['email', 'first_name', 'last_name', 'gender', 'password']

    def clean_email(self):
        """Validate that the email is unique"""
        email = self.cleaned_data.get('email')
        if Patient.objects.filter(email=email).exists():
            raise forms.ValidationError("A patient with this email already exists.")
        return email

    def save(self, commit=True):
        """Save the patient instance with the password properly stored"""
        patient = super().save(commit=False)
        # Store the password directly since the Patient model doesn't use Django's built-in password hashing
        patient.password = self.cleaned_data['password']
        
        if commit:
            patient.save()
        return patient

class PatientProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'})
    )
    height = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'})
    )
    weight = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'})
    )

    class Meta:
        model = Patient
        # Include EVERY field you want the user to be able to edit
        fields = ['first_name', 'last_name', 'email', 'gender', 'phone_number', 'address', 'date_of_birth', 'blood_group', 'height', 'weight', 'password']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50', 'type': 'date'}),
            'blood_group': forms.Select(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'}),
            'height': forms.TextInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'}),
            'weight': forms.TextInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'}),
            'password': forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 pl-12 rounded-xl border border-rose-100 focus:outline-none focus:ring-2 focus:ring-rose-300 bg-white/50'})
        }

class PharmacistRegistrationForm(forms.ModelForm):
    """
    Form for initial pharmacist registration with essential fields
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your last name'
        })
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Create a secure password'
        }),
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your email address'
        })
    )
    
    license_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your license number'
        })
    )
    
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your phone number'
        })
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Enter your address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-pink-200 focus:outline-none focus:ring-2 focus:ring-pink-300 bg-white/50',
            'placeholder': 'Create a secure password'
        }),
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )

    class Meta:
        model = Pharmacist
        fields = ['email', 'first_name', 'last_name', 'gender', 'password', 'license_number', 'phone_number', 'address']

    def clean_email(self):
        """Validate that the email is unique"""
        email = self.cleaned_data.get('email')
        if Pharmacist.objects.filter(email=email).exists():
            raise forms.ValidationError("A pharmacist with this email already exists.")
        return email

    def clean_license_number(self):
        """Validate that the license number is unique"""
        license_number = self.cleaned_data.get('license_number')
        if Pharmacist.objects.filter(license_number=license_number).exists():
            raise forms.ValidationError("A pharmacist with this license number already exists.")
        return license_number

    def save(self, commit=True):
        """Save the pharmacist instance with the password properly stored"""
        pharmacist = super().save(commit=False)
        # Store the password directly since the Pharmacist model doesn't use Django's built-in password hashing
        pharmacist.password = self.cleaned_data['password']
        
        if commit:
            pharmacist.save()
        return pharmacist