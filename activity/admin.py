from django.contrib import admin
from .models import UserActivity
# Register your models here.

@admin.register(UserActivity)
class AdminActivity(admin.ModelAdmin):
    list_display = ('user', 'action', 'target', 'created')
    list_filter = ('user',)
    date_heirarchy = ('-created')
    search_fields = ('verbs',)

