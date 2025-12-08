from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import about_view, privacy_view, terms_view, contact_view
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from entries.views import home_view

def root_dispatch(request):
    return redirect('home')


urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts
    path('accounts/', include('django.contrib.auth.urls')),  # built-in auth routes
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),  # custom accounts routes

    # Entries
    path('entries/', include(('entries.urls', 'entries'), namespace='entries')),

    # Reminders
    path('reminders/', include(('reminders.urls', 'reminders'), namespace='reminders')),

    # Subscriptions
    path('subscriptions/', include(('subscriptions.urls', 'subscriptions'), namespace='subscriptions')),

    # Static pages
    path('', root_dispatch, name='landing'),
    path('home/', home_view, name='home'),
    path('welcome/', home_view, name='welcome'),
    path('about/', about_view, name='about'),
    path('privacy/', privacy_view, name='privacy'),
    path('terms/', terms_view, name='terms'),
    path('contact/', contact_view, name='contact'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)