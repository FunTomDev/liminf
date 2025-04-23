from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name',)
    list_filter = ('subject',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'type', 'file', 'url', 'uploaded_at', 'uploaded_by')
    search_fields = ('title',)
    list_filter = ('topic', 'type')