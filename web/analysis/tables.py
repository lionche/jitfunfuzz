
import django_tables2 as tables
from .models import Testbed

class TestbedTable(tables.Table):
    class Meta:
        model = Testbed
        template_name = "django_tables2/bootstrap.html"
        # attrs = {'class': 'paleblue'}
        # fields = ("Testbed_name","Testbed_version","Testbed_location" )