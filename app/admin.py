from django.contrib import admin
from .models import Service, Testimonial
from django.contrib import admin
from .models import Staff, StaffSalary, Product, Banner


# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_address']



# gallery/admin.py
from django.contrib import admin
from .models import GalleryImage

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('category', 'place', 'event_date', 'created_at')
    list_filter = ('category', 'event_date')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'role', 'joining_date', 'is_active')  # columns shown in admin list
    search_fields = ('name', 'phone', 'role')  # search box
    list_filter = ('role', 'is_active')        # filters on right side

@admin.register(StaffSalary)
class StaffSalaryAdmin(admin.ModelAdmin):
    list_display = ("staff", "month_date", "basic_salary", "allowance", "deduction", "net_salary", "status")
    list_filter = ("status", "month_date")
    search_fields = ("staff__name",)

from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name", "rate", "image")

from django.contrib import admin
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')


