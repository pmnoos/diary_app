from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReminderListView.as_view(), name='reminder_list'),
    path('new/', views.ReminderCreateView.as_view(), name='reminder_create'),
    path('<int:pk>/edit/', views.ReminderUpdateView.as_view(), name='reminder_update'),
    path('<int:pk>/delete/', views.ReminderDeleteView.as_view(), name='reminder_delete'),
    # add any additional reminder-specific routes here
]
