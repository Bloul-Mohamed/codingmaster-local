from django.contrib import admin

# Register your models here.
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',
                    'first_name', 'last_name', 'depertment')
    search_fields = ('username', 'email')
    ordering = ('-id',)
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'depertment')
        }),
    )
