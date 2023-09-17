# Register your models here.
from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.forms import TextInput , Textarea , CharField

# Register your models here.

class userAdminConfig(UserAdmin):
    model = User
    search_fields = ('email','username','phone','gender',)
    list_filter = ('id','email','username','phone','gender','is_staff','is_active')
    list_display = ('id','email','username','phone','gender','is_staff','is_active')
    ordering = ('-start_date',)

    fieldsets = (
        (None, {'fields': ('email','username','phone','gender')}),
        ('permissions', {'fields': ('is_staff','is_active')}),
    )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }

    add_fieldsetsm = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','phone','gender','password1','password2','is_staff','is_active')
        })
    )

admin.site.register(User,userAdminConfig)