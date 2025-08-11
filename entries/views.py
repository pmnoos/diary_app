from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Entry
from .forms import EntryForm

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'entries/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 10
    
    def get_queryset(self):
        return Entry.objects.filter(author=self.request.user)

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
