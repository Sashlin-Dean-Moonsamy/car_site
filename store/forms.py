from django import forms
from .models import Inquiry, Car, CarImage
from car_site.utils.imageKit_uploader import upload_image_to_imagekit
import os
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)


# ---- Base Image Validation / Processing Mixin ----
class ImageProcessingMixin:
    """Reusable mixin for validating and processing uploaded images."""

    MAX_SIZE_MB = 5

    def clean_image(self, field_name):
        """
        Validate and process an uploaded image.
        Converts to JPEG, ensures proper format and size.
        """
        image = self.cleaned_data.get(field_name)
        if not image:
            return None

        # Validate file size
        if image.size > self.MAX_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f"Image file too large (> {self.MAX_SIZE_MB}MB)")

        # Validate content type
        if not image.content_type.startswith("image/"):
            raise forms.ValidationError("File type not supported")

        # Process image safely
        try:
            img = Image.open(image)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=95)
            output.seek(0)
            image.file = output
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise forms.ValidationError(f"Error processing image: {str(e)}")

        return image


# ---- Car Admin Form ----
class CarAdminForm(forms.ModelForm, ImageProcessingMixin):
    """
    Admin form for managing cars.
    Handles primary image upload and ImageKit integration.
    """

    primary_image_upload = forms.ImageField(
        required=False,
        label="Primary Image Upload",
        widget=forms.FileInput(attrs={"accept": "image/*"})
    )

    class Meta:
        model = Car
        fields = [
            "title",
            "make",
            "model",
            "year",
            "price",
            "mileage",
            "transmission",
            "fuel_type",
            "description",
            "featured",
            "primary_image_upload",
        ]

    def clean_primary_image_upload(self):
        return self.clean_image("primary_image_upload")

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("primary_image_upload")
        if image_file:
            try:
                file_name = os.path.splitext(image_file.name)[0] + ".jpg"
                url = upload_image_to_imagekit(image_file, file_name, folder="/cars/primary/")
                if not url:
                    raise forms.ValidationError("Failed to get image URL from ImageKit")
                # Optional: if you want a primary image_url on Car
                if hasattr(instance, "primary_image_url"):
                    instance.primary_image_url = url
            except Exception as e:
                logger.error(f"Error uploading image: {str(e)}")
                raise forms.ValidationError(f"Error uploading image: {str(e)}")
        if commit:
            instance.save()
        return instance


# ---- Car Image Admin Form ----
class CarImageAdminForm(forms.ModelForm, ImageProcessingMixin):
    """
    Admin form for managing additional car images.
    Handles validation and upload to ImageKit.
    """

    image_upload = forms.ImageField(
        required=True,
        label="Upload Car Image",
        widget=forms.FileInput(attrs={"accept": "image/*"})
    )

    class Meta:
        model = CarImage
        fields = ["car", "image_upload"]

    def clean_image_upload(self):
        return self.clean_image("image_upload")

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get("image_upload")
        if image_file:
            try:
                file_name = os.path.splitext(image_file.name)[0] + ".jpg"
                url = upload_image_to_imagekit(image_file, file_name, folder="/cars/additional/")
                if not url:
                    raise forms.ValidationError("Failed to get image URL from ImageKit")
                instance.image_url = url
            except Exception as e:
                logger.error(f"Error uploading image: {str(e)}")
                raise forms.ValidationError(f"Error uploading image: {str(e)}")
        if commit:
            instance.save()
        return instance

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your message'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone (optional)'}),
        }

        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone (optional)'}),
        }

    def save(self, commit=True):
        # For general contact, car field will be blank
        instance = super().save(commit=False)
        instance.car = None
        if commit:
            instance.save()
        return instance
