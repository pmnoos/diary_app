from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('plans/', views.subscription_plans, name='plans'),
    path('manage/', views.manage_subscription, name='manage'),
    path('upgrade/<int:plan_id>/', views.upgrade_subscription, name='upgrade'),
    path('success/', views.subscription_success, name='success'),
    path('cancel/', views.cancel_subscription, name='cancel'),
    path("features/", views.features, name="features"),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]