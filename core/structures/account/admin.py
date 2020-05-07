from django.contrib import admin
from .models import (Profile, ProfileDetail, Address, Phone, Company,
                     CompanyDetail)


class ProfileAdmin(admin.ModelAdmin):
    pass


class ProfileDetailAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


class PhoneAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass



class CompanyDetailAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileDetail, ProfileDetailAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyDetail, CompanyDetailAdmin)
