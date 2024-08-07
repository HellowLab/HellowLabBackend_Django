from django.contrib import admin

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin): 
    list_display = (['username','email','first_name','last_name','last_login'])