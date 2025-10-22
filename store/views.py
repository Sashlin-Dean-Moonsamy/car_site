from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car
from .forms import InquiryForm, ContactForm


# Create your views here.
def home(request):
    return render(request, 'store/index.html')


def browse_cars(request):
    cars = Car.objects.all()
    return render(request, 'store/brows_cars.html', {'cars': cars})


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.car = car
            inquiry.save()
            success = True
            form = InquiryForm()  # reset form after submission
        else:
            success = False
    else:
        form = InquiryForm()
        success = False

    return render(request, 'store/car_detail.html', {'car': car, 'form': form, 'success': success})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()  # reset form after submission
        else:
            success = False
    else:
        form = ContactForm()
        success = False

    return render(request, 'store/contact.html', {'form': form, 'success': success})
