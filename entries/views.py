from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Entry
from .forms import EntryForm

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'entries/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 15  # Show more entries per page for better UX
    
    def get_queryset(self):
        queryset = Entry.objects.filter(author=self.request.user)
        
        # Filter options
        view_type = self.request.GET.get('view', 'active')  # active, archived, all
        
        if view_type == 'archived':
            queryset = queryset.filter(is_archived=True)
        elif view_type == 'all':
            pass  # Show all entries
        else:  # active (default)
            queryset = queryset.filter(is_archived=False)
        
        # Time filters
        time_filter = self.request.GET.get('time', '')
        if time_filter == 'this_year':
            start_of_year = timezone.now().replace(month=1, day=1)
            queryset = queryset.filter(date__gte=start_of_year.date())
        elif time_filter == 'last_month':
            last_month = timezone.now() - timedelta(days=30)
            queryset = queryset.filter(date__gte=last_month.date())
        elif time_filter == 'this_month':
            start_of_month = timezone.now().replace(day=1)
            queryset = queryset.filter(date__gte=start_of_month.date())
        
        # Mood filter
        mood_filter = self.request.GET.get('mood', '')
        if mood_filter:
            queryset = queryset.filter(mood=mood_filter)
        
        return queryset.order_by('-date', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = self.request.GET.get('view', 'active')
        context['time_filter'] = self.request.GET.get('time', '')
        context['mood_filter'] = self.request.GET.get('mood', '')
        
        # Statistics for the user
        user_entries = Entry.objects.filter(author=self.request.user)
        context['stats'] = {
            'total': user_entries.count(),
            'active': user_entries.filter(is_archived=False).count(),
            'archived': user_entries.filter(is_archived=True).count(),
            'this_year': user_entries.filter(date__year=timezone.now().year).count(),
            'can_auto_archive': user_entries.filter(is_archived=False).exclude(date__gte=timezone.now().date() - timedelta(days=180)).count(),
        }
        
        # Popular moods
        mood_stats = user_entries.exclude(mood='').values('mood').annotate(count=Count('mood')).order_by('-count')[:5]
        context['popular_moods'] = mood_stats
        
        return context

class EntryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'
    context_object_name = 'entry'
    
    def test_func(self):
        entry = self.get_object()
        return entry.author == self.request.user

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your diary entry has been created!')
        return super().form_valid(form)

class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_form.html'
    
    def test_func(self):
        entry = self.get_object()
        return entry.author == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your diary entry has been updated!')
        return super().form_valid(form)

class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = 'entries/entry_confirm_delete.html'
    success_url = reverse_lazy('entry_list')
    
    def test_func(self):
        entry = self.get_object()
        return entry.author == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your diary entry has been deleted!')
        return super().delete(request, *args, **kwargs)

# Demo Views - Read-only access to demo user's entries
def demo_entries_view(request):
    """Show demo entries from a demo user account (read-only)"""
    try:
        demo_user = User.objects.get(username='demo_user')
        demo_entries = Entry.objects.filter(author=demo_user).order_by('-created_at')[:5]  # Show last 5 entries
    except User.DoesNotExist:
        demo_entries = []
    
    context = {
        'entries': demo_entries,
        'is_demo': True,
        'demo_message': "This is a preview of what your diary could look like. Create an account to start your own private diary!"
    }
    return render(request, 'entries/demo_entry_list.html', context)

def demo_entry_detail_view(request, pk):
    """Show a specific demo entry (read-only)"""
    try:
        demo_user = User.objects.get(username='demo_user')
        entry = get_object_or_404(Entry, pk=pk, author=demo_user)
    except User.DoesNotExist:
        entry = None
    
    context = {
        'entry': entry,
        'is_demo': True,
        'demo_message': "This is a sample diary entry. Create your account to write your own!"
    }
    return render(request, 'entries/demo_entry_detail.html', context)


# New Archive and Search functionality
class EntrySearchView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'entries/search_results.html'
    context_object_name = 'entries'
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Entry.objects.filter(author=self.request.user)
        
        if query:
            # Search in title, content, and tags
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__icontains=query)
            ).distinct()
        
        # Additional filters
        include_archived = self.request.GET.get('include_archived', '') == 'on'
        if not include_archived:
            queryset = queryset.filter(is_archived=False)
        
        mood_filter = self.request.GET.get('mood', '')
        if mood_filter:
            queryset = queryset.filter(mood=mood_filter)
        
        # Date range filters
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        return queryset.order_by('-date', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['include_archived'] = self.request.GET.get('include_archived', '') == 'on'
        context['mood_filter'] = self.request.GET.get('mood', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        context['total_results'] = self.get_queryset().count()
        return context


@login_required
def toggle_archive_entry(request, pk):
    """Toggle archive status of an entry"""
    entry = get_object_or_404(Entry, pk=pk, author=request.user)
    
    if entry.is_archived:
        entry.unarchive()
        messages.success(request, f'"{entry.title}" has been restored from archive.')
    else:
        entry.archive()
        messages.success(request, f'"{entry.title}" has been archived.')
    
    # Redirect back to where they came from
    return redirect(request.META.get('HTTP_REFERER', 'entry_list'))


@login_required
def bulk_archive_view(request):
    """Bulk archive old entries"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'auto_archive':
            # Auto-archive entries older than 6 months
            six_months_ago = timezone.now().date() - timedelta(days=180)
            old_entries = Entry.objects.filter(
                author=request.user,
                is_archived=False,
                date__lt=six_months_ago
            )
            count = old_entries.count()
            
            for entry in old_entries:
                entry.archive()
            
            messages.success(request, f'Successfully archived {count} old entries!')
            
        elif action == 'archive_selected':
            entry_ids = request.POST.getlist('entry_ids')
            entries = Entry.objects.filter(id__in=entry_ids, author=request.user)
            count = 0
            
            for entry in entries:
                if not entry.is_archived:
                    entry.archive()
                    count += 1
            
            messages.success(request, f'Successfully archived {count} entries!')
        
        return redirect('entry_list')
    
    # Show entries that can be archived
    year_filter = request.GET.get('year')
    if year_filter:
        try:
            year_filter = int(year_filter)
            eligible_entries = Entry.objects.filter(
                author=request.user,
                is_archived=False,
                date__year=year_filter
            ).order_by('date')
        except ValueError:
            eligible_entries = Entry.objects.none()
    else:
        eligible_entries = Entry.objects.filter(
            author=request.user,
            is_archived=False,
            date__lt=timezone.now().date() - timedelta(days=180)
        ).order_by('date')
    
    cutoff_date = timezone.now().date() - timedelta(days=180)
    
    context = {
        'eligible_entries': eligible_entries,
        'year_filter': year_filter,
        'cutoff_date': cutoff_date,
    }
    
    return render(request, 'entries/bulk_archive.html', context)


@login_required
def archive_dashboard(request):
    """Dashboard showing archive statistics and management options"""
    user_entries = Entry.objects.filter(author=request.user)
    
    # Basic statistics
    total_entries = user_entries.count()
    archived_entries = user_entries.filter(is_archived=True).count()
    active_entries = user_entries.filter(is_archived=False).count()
    can_auto_archive = user_entries.filter(
        is_archived=False,
        date__lt=timezone.now().date() - timedelta(days=180)
    ).count()
    
    # Generate yearly statistics for the yearly breakdown section
    yearly_data = {}
    for entry in user_entries:
        year = entry.date.year
        if year not in yearly_data:
            yearly_data[year] = {
                'year': year,
                'total': 0,
                'archived': 0,
                'active': 0,
                'eligible': 0
            }
        
        yearly_data[year]['total'] += 1
        if entry.is_archived:
            yearly_data[year]['archived'] += 1
        else:
            yearly_data[year]['active'] += 1
            # Check if this entry is eligible for archiving (6+ months old)
            if entry.date < timezone.now().date() - timedelta(days=180):
                yearly_data[year]['eligible'] += 1
    
    # Convert to sorted list
    yearly_stats = sorted(yearly_data.values(), key=lambda x: x['year'], reverse=True)
    
    # Get recently archived entries
    recently_archived = user_entries.filter(is_archived=True).order_by('-archived_at')[:5]
    
    context = {
        'total_entries': total_entries,
        'archived_entries': archived_entries, 
        'active_entries': active_entries,
        'can_auto_archive': can_auto_archive,
        'yearly_stats': yearly_stats,
        'recently_archived': recently_archived,
    }
    
    return render(request, 'entries/archive_dashboard.html', context)
