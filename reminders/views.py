from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Reminder
from entries.models import Entry


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'reminders/reminder_list.html'
    context_object_name = 'reminders'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Reminder.objects.filter(author=self.request.user)
        
        # Filter options
        filter_type = self.request.GET.get('filter', 'upcoming')
        
        if filter_type == 'today':
            queryset = queryset.filter(date=timezone.now().date())
        elif filter_type == 'this_week':
            today = timezone.now().date()
            week_end = today + timezone.timedelta(days=7)
            queryset = queryset.filter(date__range=[today, week_end])
        elif filter_type == 'overdue':
            queryset = queryset.filter(date__lt=timezone.now().date(), is_completed=False)
        elif filter_type == 'completed':
            queryset = queryset.filter(is_completed=True)
        elif filter_type == 'all':
            pass  # Show all
        else:  # upcoming (default)
            queryset = queryset.filter(date__gte=timezone.now().date(), is_completed=False)
        
        return queryset.order_by('date', 'time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'upcoming')
        
        # Quick stats
        user_reminders = Reminder.objects.filter(author=self.request.user)
        context['stats'] = {
            'total': user_reminders.count(),
            'today': user_reminders.filter(date=timezone.now().date(), is_completed=False).count(),
            'this_week': user_reminders.filter(
                date__range=[timezone.now().date(), timezone.now().date() + timezone.timedelta(days=7)],
                is_completed=False
            ).count(),
            'overdue': user_reminders.filter(date__lt=timezone.now().date(), is_completed=False).count(),
        }
        
        return context


class ReminderDetailView(LoginRequiredMixin, DetailView):
    model = Reminder
    template_name = 'reminders/reminder_detail.html'
    context_object_name = 'reminder'
    
    def get_queryset(self):
        return Reminder.objects.filter(author=self.request.user)


class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    template_name = 'reminders/reminder_form.html'
    fields = ['title', 'description', 'date', 'time', 'category', 'priority', 
              'alert_preference', 'location']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Reminder "{form.instance.title}" created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('reminder_list')


class ReminderUpdateView(LoginRequiredMixin, UpdateView):
    model = Reminder
    template_name = 'reminders/reminder_form.html'
    fields = ['title', 'description', 'date', 'time', 'category', 'priority', 
              'alert_preference', 'location', 'is_completed']
    
    def get_queryset(self):
        return Reminder.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f'Reminder "{form.instance.title}" updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('reminder_detail', kwargs={'pk': self.object.pk})


class ReminderDeleteView(LoginRequiredMixin, DeleteView):
    model = Reminder
    template_name = 'reminders/reminder_confirm_delete.html'
    context_object_name = 'reminder'
    success_url = reverse_lazy('reminder_list')
    
    def get_queryset(self):
        return Reminder.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        reminder = self.get_object()
        messages.success(request, f'Reminder "{reminder.title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
def toggle_reminder_complete(request, pk):
    """Toggle reminder completion status"""
    reminder = get_object_or_404(Reminder, pk=pk, author=request.user)
    
    if reminder.is_completed:
        reminder.is_completed = False
        reminder.completed_at = None
        messages.success(request, f'Reminder "{reminder.title}" marked as incomplete.')
    else:
        reminder.mark_completed()
        messages.success(request, f'Reminder "{reminder.title}" marked as completed! 🎉')
    
    reminder.save()
    return redirect('reminder_list')


@login_required
def reminder_dashboard(request):
    """Dashboard showing reminder overview and quick stats"""
    user_reminders = Reminder.objects.filter(author=request.user)
    today = timezone.now().date()
    
    # Get different categories of reminders
    context = {
        'today_reminders': user_reminders.filter(date=today, is_completed=False),
        'overdue_reminders': user_reminders.filter(date__lt=today, is_completed=False),
        'upcoming_reminders': user_reminders.filter(
            date__gt=today, 
            date__lte=today + timezone.timedelta(days=7),
            is_completed=False
        )[:5],
        'recent_completed': user_reminders.filter(is_completed=True).order_by('-completed_at')[:3],
    }
    
    return render(request, 'reminders/dashboard.html', context)
