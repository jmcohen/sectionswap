from django.contrib import admin
from swap.models import *

class CourseAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Course, CourseAdmin)