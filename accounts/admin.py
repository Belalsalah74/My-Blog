from accounts.models import Profile
from django.contrib import admin




@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_select_related = ['user']
    fields = ['img','user']


