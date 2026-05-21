from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # ile pustych formularzy ma się pojawić


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = [CarModelInline]


class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "car_make", "type", "year")
    list_filter = ("car_make", "type", "year")


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
