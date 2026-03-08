from django.contrib import admin
from django.db.models import QuerySet
from .models import Patient, Appointment, Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user_username', 'specialization')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctors', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient_first_name', 'patient_last_name')
    ordering = ('-date',)

    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_confirmed.short_description = "Mark selected appointments as CONFIRMED"

    def mark_completed(self, request, queryset):
        queryset.update(status='Completed')
    mark_completed.short_description = "Mark selected appointments as COMPELTED"

    def mark_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
    mark_cancelled.short_description ="Mark selected appointments as CANCELLED"    



    