from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from medservices.models import CustomUser

from .models import Blood_bank, Hospital, Doctor

# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
# admin.site.register(Appointment)


# admin.site.register(Hospital)
# admin.site.register(Doctor)
# admin.site.register(Blood_bank)
