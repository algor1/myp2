from django.contrib import admin

# Register your models here.

from .models import Images, Task

admin.site.register(Images)
admin.site.register(Task)
