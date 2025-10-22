from django import forms
from .models import Inquiry

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
