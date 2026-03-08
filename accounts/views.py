from django.forms import EmailField
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from clinic.views import appointment_success
from .forms import UserRegisterForm
from clinic.models import Appointment, Patient
from django.utils import timezone


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            #create patient profile
            Patient.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone_number=form.cleaned_data['phone_number'],
            )

            login(request, user)
            return redirect('dashboard')
        else:
            print(form.errors)

    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
        
# login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if hasattr(user, 'doctor'):
                return redirect('doctor_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out.")
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):

    if hasattr(request.user, 'doctor'):
        return redirect('doctor_dashboard')
    

    patient, created = Patient.objects.get_or_create(
        user=request.user,
        defaults={
            'first_name': request.user.first_name or request.user.username,
            'last_name': request.user.last_name or '',
            'email': request.user.email,
            'phone_number': '',
        }
    )

    appointments = Appointment.objects.filter(patient=patient).order_by('-date')

    total_appointments = appointments.count()
    upcoming_appointments = appointments.filter(status='Pending').count()
    completed_appointments = appointments.filter(status='completed').count()

    context = {
        'appointments': appointments,
        'total_appointments': total_appointments,
        'upcoming_appointments': upcoming_appointments,
        'completed_appointments': completed_appointments,
    }
    return render(request, 'accounts/dashboard.html', context)