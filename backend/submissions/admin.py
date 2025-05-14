from django.contrib import admin

from .models import Problem, Solution

# Register your models here.
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)