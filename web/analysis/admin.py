from django.contrib import admin
from .models import Testbed


class TestbedManager(admin.ModelAdmin):
    list_display = ['id', 'Testbed_name', 'Testbed_version', 'Testbed_location', 'Remark']
    list_display_links = ['id', 'Testbed_name']
    list_filter = ['Testbed_name']
    search_fields = ['Testbed_name']
    # list_editable = ['Remark']

admin.site.register(Testbed, TestbedManager)
