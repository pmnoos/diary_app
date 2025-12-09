from django.urls import path
from . import views

app_name = 'reminders'

urlpatterns = [
    path('', views.ReminderListView.as_view(), name='reminder_dashboard'),
    path('new/', views.ReminderCreateView.as_view(), name='reminder_create'),
    path('<int:pk>/edit/', views.ReminderUpdateView.as_view(), name='reminder_update'),
    path('<int:pk>/delete/', views.ReminderDeleteView.as_view(), name='reminder_delete'),
    # add any additional reminder-specific routes here
        path('<int:pk>/', views.ReminderDetailView.as_view(), name='reminder_detail'),
    path('toggle/<int:pk>/', views.toggle_reminder_complete, name='reminder_toggle'),
    ]