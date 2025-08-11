from django.urls import path
from . import views

urlpatterns = [
    path('', views.EntryListView.as_view(), name='entry_list'),
    path('new/', views.EntryCreateView.as_view(), name='entry_create'),
    path('<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),
    # Demo URLs - accessible without login
    path('demo/', views.demo_entries_view, name='demo_entries'),
    path('demo/<int:pk>/', views.demo_entry_detail_view, name='demo_entry_detail'),
]