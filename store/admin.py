from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarImage
from .forms import CarAdminForm, CarImageAdminForm


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    form = CarAdminForm
    list_display = ('title', 'make', 'model', 'year', 'price', 'featured', 'primary_image_preview')
    search_fields = ('title', 'make', 'model', 'year')
    list_filter = ('make', 'featured', 'year')
    ordering = ('-created_at',)

    def primary_image_preview(self, obj):
        """
        Show the car's primary image in the admin list view.
        """
        if hasattr(obj, 'primary_image_url') and obj.primary_image_url:
            return format_html('<img src="{}" style="height: 60px;" />', obj.primary_image_url)
        return "-"
    primary_image_preview.short_description = 'Primary Image'


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    form = CarImageAdminForm
    list_display = ('car', 'image_preview', 'uploaded_at')
    search_fields = ('car__title',)
    list_filter = ('car__make',)

    def image_preview(self, obj):
        """
        Show thumbnail of uploaded car image in admin list view.
        """
        if obj.image_url:
            return format_html('<img src="{}" style="height: 50px;" />', obj.image_url)
        return "-"
    image_preview.short_description = 'Image'
