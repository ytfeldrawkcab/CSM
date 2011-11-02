from csm.models import *
from django.contrib import admin

class IndividualInline(admin.TabularInline):
    model = Individual
    extra = 1

class OwnerAdmin(admin.ModelAdmin):
    fields = ['username', 'password']
    inlines = [IndividualInline]

admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerType)

admin.site.register(Election)
admin.site.register(Candidate)
