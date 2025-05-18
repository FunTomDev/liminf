from django.contrib import admin

from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'account_type', 'bio')
    search_fields = ('username', 'email')
    list_filter = ('account_type',)
    ordering = ('username',)
