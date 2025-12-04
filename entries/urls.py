from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Diary entry CRUD
    path('', views.EntryListView.as_view(), name='entry_list'),
    path('new/', views.EntryCreateView.as_view(), name='entry_create'),
    path('<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),

    # Archive & Search
    path('search/', views.EntrySearchView.as_view(), name='entry_search'),
    path('<int:pk>/toggle-archive/', views.toggle_archive_entry, name='toggle_archive_entry'),
    path('bulk-archive/', views.bulk_archive_view, name='bulk_archive'),
    path('archive-dashboard/', views.archive_dashboard, name='archive_dashboard'),

    # Offline / demo
    path('offline/', TemplateView.as_view(template_name='entries/offline.html'), name='offline'),
    path('demo/', views.demo_entries_view, name='demo_entries'),
    path('demo/<int:pk>/', views.demo_entry_detail_view, name='demo_entry_detail'),

    # PWA Service Worker
    path('sw.js', TemplateView.as_view(
        template_name="entries/sw.js",
        content_type='application/javascript'
    ), name='sw.js'),
]
