from django.contrib import admin
from .models import UserProfile, Complaint, Feedback


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'mobile_number', 'is_admin')
    search_fields = ('full_name', 'email', 'mobile_number')
    list_filter = ('is_admin',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'complaint_type', 'location', 'submitted_at', 'verified')
    list_filter = ('complaint_type', 'verified', 'submitted_at')
    search_fields = ('description', 'location', 'user__full_name', 'user__email')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'suggestion', 'submitted_at', 'is_visible')
    list_editable = ('is_visible',)
    search_fields = ('user__full_name', 'user__email', 'suggestion')
    list_filter = ('submitted_at', 'is_visible')
    date_hierarchy = 'submitted_at'

