from django.contrib import admin
from app.models import *
# Register your models here.

class AdminPerson(admin.ModelAdmin):
    list_display = ['fio','age']

class AdminPolls(admin.ModelAdmin):
    list_display = ['name','startdate','max_count']


admin.site.register(Person,AdminPerson);
admin.site.register(Polls,AdminPolls);