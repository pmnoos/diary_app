from django.shortcuts import render
from django.utils import timezone

def home_view(request):
    context = {
        'current_date': timezone.now()
    }
    return render(request, 'home.html', context)
