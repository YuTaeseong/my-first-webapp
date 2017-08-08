from django.contrib import admin

# Register your models here.
from .models import Data_Base, Data_SeongSu, Data_Digital, Site_Name

admin.site.register(Data_Digital)
admin.site.register(Data_SeongSu)
admin.site.register(Data_Base)
admin.site.register(Site_Name)