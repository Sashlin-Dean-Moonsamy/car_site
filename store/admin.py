from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarImage
from .forms import CarAdminForm, CarImageAdminForm

@admin.register(Car)
class ProductAdmin(admin.ModelAdmin):
    form = CarAdminForm
    list_display = ('name', 'price', 'primary_image_preview')

    def primary_image_preview(self, obj):
        if obj.primary_image_url:
            return format_html('<img src="{}" style="height: 60px;" />', obj.primary_image_url)
        return "-"
    primary_image_preview.short_description = 'Primary Image'


@admin.register(CarImage)
class ProductImageAdmin(admin.ModelAdmin):
    form = CarImageAdminForm
    list_display = ('product', 'order', 'image_preview')

    def image_preview(self, obj):
        return format_html('<img src="{}" style="height: 50px;" />', obj.image_url)
    image_preview.short_description = 'Image'