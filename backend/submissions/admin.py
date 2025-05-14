from django.contrib import admin

from .models import Problem, Solution

# Register your models here.
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('topic',)

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)