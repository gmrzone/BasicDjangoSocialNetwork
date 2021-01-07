from django.contrib import admin
from .models import ImagePost

# Register your models here.

@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image', 'created')
    list_filter = ('created',)
    search_fields = ('title', 'description')


        