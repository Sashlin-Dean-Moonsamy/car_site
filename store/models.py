from django.db import models
from django.utils import timezone
from car_site.utils.imageKit_uploader import upload_image_to_imagekit

# Helper for image upload paths
def car_image_upload_path(instance, filename):
    return f"cars/{instance.car.id}/{filename}"

class Car(models.Model):
    """Represents a car listing."""
    title = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    transmission = models.CharField(max_length=50, blank=True, null=True)
    fuel_type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

    class Meta:
        ordering = ['-created_at']


class CarImage(models.Model):
    """Stores multiple images per car."""
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image_url =  models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car.title}"
    

class Inquiry(models.Model):
    """Stores customer inquiries or orders sent from the site."""
    car = models.ForeignKey(Car, related_name='inquiries', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry from {self.name} about {self.car.title}"
