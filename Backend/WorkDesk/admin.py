from django.contrib import admin
from .models import Admin,Technicians,Task

# Register your models here.
admin.site.register(Admin)
admin.site.register(Technicians)
admin.site.register(Task)