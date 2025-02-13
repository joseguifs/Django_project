from django.contrib import admin
from cars.models import Car, Brand


# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',) # quais campos do modelo Brand e o valor de cada instância de Brand serão exibido no painel administrativo 
    search_fields = ('name',) # adiciona um campo de busca na interface administrativa

class CarAdmin(admin.ModelAdmin):
    list_display = ('model','brand','factory_year','model_year','value')
    search_fields = ('model','brand')


admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)