from django.urls import path
from . import views

urlpatterns = [
    path('', views.reminder_dashboard, name='reminder_dashboard'),
    path('list/', views.ReminderListView.as_view(), name='reminder_list'),
    path('create/', views.ReminderCreateView.as_view(), name='reminder_create'),
    path('<int:pk>/', views.ReminderDetailView.as_view(), name='reminder_detail'),
    path('<int:pk>/edit/', views.ReminderUpdateView.as_view(), name='reminder_update'),
    path('<int:pk>/delete/', views.ReminderDeleteView.as_view(), name='reminder_delete'),
    path('<int:pk>/toggle/', views.toggle_reminder_complete, name='reminder_toggle'),
]
