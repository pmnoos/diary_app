#!/usr/bin/env python
"""
Seed script to create sample reminders for testing.
Run with: python seed_reminders.py
"""

import os
import django
from datetime import datetime, timedelta, date, time
from random import choice, randint

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from reminders.models import Reminder

# Sample reminder data
REMINDER_TITLES = [
    "Doctor Appointment",
    "Team Meeting",
    "Call Mom",
    "Grocery Shopping",
    "Gym Workout",
    "Book Club Meeting",
    "Car Service",
    "Birthday Party",
    "Project Deadline",
    "Dentist Checkup",
    "Pay Bills",
    "Weekly Review",
    "Coffee with Sarah",
    "Submit Report",
    "Pick up Dry Cleaning",
    "Oil Change",
    "Family Dinner",
    "Yoga Class",
    "Client Presentation",
    "Vacation Planning",
    "Home Maintenance",
    "Study Session",
    "Tax Preparation",
    "Garden Watering",
    "Medication Refill",
]

DESCRIPTIONS = [
    "Don't forget to bring insurance card and list of current medications.",
    "Prepare agenda items and review last meeting's action points.",
    "Check in and see how she's doing. Ask about her garden project.",
    "Need: milk, bread, eggs, vegetables, and cleaning supplies.",
    "Leg day - focus on squats and lunges. Don't skip warm-up!",
    "This month's book: 'The Seven Husbands of Evelyn Hugo'",
    "Regular maintenance check - oil change and tire rotation.",
    "Buy gift and wrap it. Remember to RSVP by Thursday.",
    "Final submission for Q3 analysis. Include charts and recommendations.",
    "6-month checkup. Confirm appointment time the day before.",
    "Utilities, internet, phone bill, and credit card payment.",
    "Review goals, accomplishments, and plan for next week.",
    "Catch up on work projects and weekend plans.",
    "Monthly sales report with client feedback analysis.",
    "Suits for next week's conference presentations.",
    "Car is due for maintenance. Check if appointment is confirmed.",
    "Sunday dinner at grandparents'. Bring dessert.",
    "Morning class - remember yoga mat and water bottle.",
    "Present quarterly results to potential new clients.",
    "Research destinations and book flights for summer trip.",
    "Check HVAC filters and clean gutters before winter.",
    "Review chapter 5-7 for upcoming exam next week.",
    "Gather documents: W2s, receipts, and bank statements.",
    "Water plants and check for any pest issues.",
    "Prescription expires this week - call pharmacy to refill.",
]

CATEGORIES = ['personal', 'work', 'health', 'social', 'finance', 'other']
PRIORITIES = ['low', 'medium', 'high']
ALERT_PREFERENCES = ['none', 'day_of', '1_day', '3_days', '1_week']

def create_sample_reminders():
    """Create sample reminders spanning different time periods."""
    
    # Get all users and let user choose
    users = User.objects.all()
    if not users:
        print("❌ No users found. Please create a user account first.")
        return
    
    print("👥 Available users:")
    for i, user in enumerate(users, 1):
        reminder_count = Reminder.objects.filter(author=user).count()
        print(f"   {i}. {user.username} (currently has {reminder_count} reminders)")
    
    # Let user choose which account to populate
    while True:
        try:
            choice = input(f"\n🎯 Which user account should get the sample reminders? (1-{len(users)} or 'all'): ").strip().lower()
            if choice == 'all':
                selected_users = list(users)
                break
            else:
                choice_num = int(choice)
                if 1 <= choice_num <= len(users):
                    selected_users = [users[choice_num - 1]]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(users)}")
        except ValueError:
            print("Please enter a valid number or 'all'")
    
    for user in selected_users:
        print(f"\n⏰ Creating sample reminders for user: {user.username}")
        
        # Check existing reminders
        existing_count = Reminder.objects.filter(author=user).count()
        if existing_count > 0:
            response = input(f"⚠️  Found {existing_count} existing reminders for {user.username}. Delete them? (y/N): ")
            if response.lower() == 'y':
                Reminder.objects.filter(author=user).delete()
                print("🗑️  Existing reminders deleted.")

        reminders_created = 0
        today = date.today()
        
        # 1. Overdue reminders (past dates)
        print("⚠️  Creating overdue reminders...")
        for i in range(3):
            reminder_date = today - timedelta(days=randint(1, 14))
            create_reminder(user, reminder_date, is_overdue=True)
            reminders_created += 1
        
        # 2. Today's reminders
        print("📅 Creating today's reminders...")
        for i in range(2):
            create_reminder(user, today, is_today=True)
            reminders_created += 1
        
        # 3. Upcoming reminders (next 30 days)
        print("📆 Creating upcoming reminders...")
        for i in range(12):
            reminder_date = today + timedelta(days=randint(1, 30))
            create_reminder(user, reminder_date, is_upcoming=True)
            reminders_created += 1
        
        # 4. Future reminders (next month and beyond)
        print("🔮 Creating future reminders...")
        for i in range(8):
            reminder_date = today + timedelta(days=randint(31, 90))
            create_reminder(user, reminder_date, is_future=True)
            reminders_created += 1
        
        # 5. Completed reminders (mix of dates)
        print("✅ Creating completed reminders...")
        for i in range(5):
            reminder_date = today - timedelta(days=randint(1, 30))
            create_reminder(user, reminder_date, is_completed=True)
            reminders_created += 1
        
        print(f"✅ Created {reminders_created} sample reminders for {user.username}!")
    
    # Final summary
    total_reminders = Reminder.objects.count()
    print(f"\n📊 Final database summary:")
    print(f"   • Total reminders in database: {total_reminders}")
    for user in User.objects.all():
        user_reminders = Reminder.objects.filter(author=user).count()
        completed_count = Reminder.objects.filter(author=user, is_completed=True).count()
        pending_count = user_reminders - completed_count
        print(f"   • {user.username}: {user_reminders} reminders ({pending_count} pending, {completed_count} completed)")
    
    print(f"\n🎯 Now you can test:")
    print(f"   • Reminder list: View all reminders with filtering")
    print(f"   • Dashboard: See statistics and urgent reminders") 
    print(f"   • Complete/reopen: Toggle reminder status")
    print(f"   • Edit/delete: Manage individual reminders")

def create_reminder(user, reminder_date, is_overdue=False, is_today=False, is_upcoming=False, is_future=False, is_completed=False):
    """Create a single reminder with realistic content."""
    
    title = choice(REMINDER_TITLES)
    description = choice(DESCRIPTIONS)
    category = choice(CATEGORIES)
    priority = choice(PRIORITIES)
    alert_pref = choice(ALERT_PREFERENCES)
    
    # Adjust priority based on type
    if is_overdue or is_today:
        priority = choice(['medium', 'high', 'high'])  # Higher chance of high priority
    elif is_upcoming:
        priority = choice(['low', 'medium', 'high'])  # Even distribution
    else:
        priority = choice(['low', 'low', 'medium'])  # Lower priority for future
    
    # Add time for some reminders
    due_time = None
    if randint(1, 3) == 1:  # 33% chance of having a specific time
        hour = choice([9, 10, 11, 14, 15, 16, 17, 18, 19])
        minute = choice([0, 15, 30, 45])
        due_time = time(hour, minute)
    
    # Create the reminder
    reminder = Reminder.objects.create(
        author=user,
        title=title,
        description=description,
        date=reminder_date,
        time=due_time,
        category=category,
        priority=priority,
        alert_preference=alert_pref,
    )
    
    # Mark as completed if needed
    if is_completed:
        reminder.is_completed = True
        reminder.completed_at = datetime.now()
        reminder.save()
    
    return reminder

if __name__ == "__main__":
    print("⏰ Reminder Seed Script")
    print("=" * 50)
    create_sample_reminders()
