from django.contrib import admin

# Register your models here.
from .models import Stadium, Department, Schedule, checks


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'capacity', 'is_active')
    search_fields = ('name',)
    ordering = ('-id',)
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'capacity', 'is_active')
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-id',)
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'date',
                    'start_time', 'end_time', 'is_active', 'stadium')
    search_fields = ('department__name',)
    ordering = ('-id',)
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('department', 'date', 'start_time', 'end_time', 'is_active', 'stadium')
        }),
    )


@admin.register(checks)
class ChecksAdmin(admin.ModelAdmin):
    list_display = ('id', 'counter', 'depertment', 'stadium')
    search_fields = ('depertment__name',)
    ordering = ('-id',)
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('counter', 'depertment', 'stadium')
        }),
    )
