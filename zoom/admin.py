from django.contrib import admin
from zoom.models import *

#admin .site .register(task)
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=[
        'title','description','status',
    ]
    list_per_page=5
    search_fields=('title',)