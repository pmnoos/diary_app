from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm
from .models import ContactMessage

def home_view(request):
    context = {
        'current_date': timezone.localdate()
    }
    return render(request, 'home.html', context)

def about_view(request):
    return render(request, 'about.html')

def privacy_view(request):
    return render(request, 'privacy.html')

def terms_view(request):
    return render(request, 'terms.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            # Send email
            send_mail(
                subject=f"New Contact Message from {form.cleaned_data['name']}",
                message=f"Name: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\n\nMessage:\n{form.cleaned_data['message']}",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=['admin@example.com'],  # Change to your admin email
                fail_silently=True,
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            form = ContactForm()  # Reset form after success
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})