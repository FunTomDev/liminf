from django.contrib import admin
from .models import Material

# Register your models here.
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'type', 'file', 'url', 'uploaded_at', 'uploaded_by')
    search_fields = ('title',)
    list_filter = ('topic', 'type')
