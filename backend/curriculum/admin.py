from django.contrib import admin

from .models import Subject, Topic

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
