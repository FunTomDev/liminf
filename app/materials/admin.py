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
    list_display = ('title', 'topic', 'material_type', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('topic', 'material_type')

@admin.register(MathproArticle)
class MathproArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'url')
    search_fields = ('title', 'topic__name')
    list_filter = ('topic',)
