from django.contrib import admin
from .models import User, MP3File

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_active")

@admin.register(MP3File)
class MP3FileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "uploaded_at")