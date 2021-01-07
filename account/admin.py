from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo')
    search_fields = ('user',)
    date_hierarchy = 'updated'
    ordering = ('updated',)
    list_filter = ('user',)
