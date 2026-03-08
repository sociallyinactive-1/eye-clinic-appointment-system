from os import name
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .forms import AppointmentForm
from .models import Patient, Appointment, Doctor
from django.contrib.auth.decorators import login_required

@login_required
def doctor_dashboard(request):

    if not hasattr(request.user, 'doctor'):
        return redirect('home')
    
    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctors=doctor)

    return render(request, 'clinic/doctor_dashboard.html', {
        'appointments': appointments
    })

@login_required(login_url='login')
def book_appointment(request):
    patient, created = Patient.objects.get_or_create(
        user=request.user,
        defaults={
            'first_name': request.user.first_name or request.user.username,
            'last_name': request.user.last_name or '',
            'email': request.user.email,
            'phone_number': '',
        }
    )

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            return redirect('appointment_success')
    else:
        form = AppointmentForm()

    return render(request, 'clinic/book_appointment.html', {'form':form})


def appointment_success(request):
    return render(request, 'clinic/appointment_success.html')

@login_required
def update_status(request, appointment_id):
    if not hasattr(request.user, 'doctor'):
        return redirect('home')
    
    doctor = request.user.doctor
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        appointment.status = new_status
        appointment.save()
        return redirect('doctor_dashboard')
    
    return render(request, 'clinic/update_status.html', {
        'appointment': appointment
    })

def login_redirect(request):
    if hasattr(request.user, 'doctor'):
        return redirect('doctor_dashboard')
    elif hasattr(request.user, 'patient'):
        return redirect('home')
    else:
        return redirect('home')