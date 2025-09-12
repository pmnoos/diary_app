from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home_view, about_view, privacy_view, terms_view, contact_view
from entries.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # built-in auth routes
    path('accounts/', include('accounts.urls')),  # custom accounts routes (signup)
    path('entries/', include('entries.urls')),  # diary entries routes
    path('reminders/', include('reminders.urls')),  # reminder system routes
    path('subscriptions/', include('subscriptions.urls')),  # subscription management
    path('', landing, name='landing'),
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