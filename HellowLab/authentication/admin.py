from django.contrib import admin
from .models import *

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin): 
    list_display = (['username','email','first_name','last_name','last_login'])

admin.site.register(Friendship)


