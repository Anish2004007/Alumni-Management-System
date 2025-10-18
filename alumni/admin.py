from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Alumni, Event, Announcement

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'graduation_year', 'profession', 'contact_number')
    search_fields = ('name', 'email', 'graduation_year', 'profession')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at')
    search_fields = ('title',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at')
    search_fields = ('title',)
