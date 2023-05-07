from django.contrib import admin
from .models import User, Prescription, Schedule, DrugDetail, DrugHour, PillData

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'userId',
        'userRealName',
        'userEmail',
        'userRegisterDatetime',
    )

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        'prescId',
        'prescDate',
        'dispensary'
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'startDate',
        'endDate',
        'prescId',
    )
@admin.register(DrugDetail)
class DrugDetailAdmin(admin.ModelAdmin):
    list_display = (
        'drugNo',
        'drugName',
        'drugEffect',
        'dosagePerOnce',
        'dailyDose',
        'totalDosingDays',
        'scheduleId',
    )

@admin.register(DrugHour)
class DrugHourAdmin(admin.ModelAdmin):
    list_display = (
        'scheduleId',
        'drugId',
        'hour',
    )

@admin.register(PillData)
class PillDataAdmin(admin.ModelAdmin):
    list_display = (
        'prescId',
        'pillShape',
        'pillColor',
        'pillText',
    )