from django.contrib import admin

from .models import Subject, Topic, Semester

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

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('degree_type', 'number')
    search_fields = ('degree_type',)
    list_filter = ('number',)