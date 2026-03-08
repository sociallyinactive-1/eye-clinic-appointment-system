from  django.db import models
from django.conf import settings

#doctor model
class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"
    

# patient model 
class Patient(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    email = models.EmailField() 
    phone_number = models.CharField(max_length=20) 
    date_of_birth = models.DateField(null=True, blank=True) 
    
    def __str__(self): 
        return f"{self.first_name} {self.last_name}"

# appointment model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctors = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True )
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.patient} - {self.date} {self.time}"
