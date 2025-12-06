from django.urls import path
from . import views

app_name = 'reminders'

urlpatterns = [
    path('', views.ReminderListView.as_view(), name='reminder_list'),
    path('new/', views.ReminderCreateView.as_view(), name='reminder_create'),
    path('<int:pk>/edit/', views.ReminderUpdateView.as_view(), name='reminder_edit'),
    path('<int:pk>/', views.ReminderDetailView.as_view(), name='reminder_detail'),
    path('<int:pk>/toggle/', views.reminder_toggle, name='reminder_toggle'),
    
]
