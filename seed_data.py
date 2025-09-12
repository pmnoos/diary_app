#!/usr/bin/env python
"""
Seed script to populate the diary with sample entries for testing archive functionality.
Run with: python seed_data.py
"""

import os
import django
from datetime import datetime, timedelta
from random import choice, randint

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from entries.models import Entry

# Sample data for realistic diary entries
TITLES = [
    "Morning Coffee Thoughts",
    "Weekend Adventure",
    "Learning Something New",
    "Rainy Day Reflections",
    "Family Time",
    "Work Achievements",
    "Travel Memories",
    "Cooking Experiment",
    "Book Club Discussion",
    "Garden Progress",
    "Movie Night",
    "Exercise Journey",
    "Creative Project",
    "Friendship Moments",
    "Seasonal Changes",
    "Personal Growth",
    "Technology Discoveries",
    "Music and Memories",
    "Pet Adventures",
    "Life Lessons",
    "Dream Journal",
    "Goal Setting",
    "Gratitude Practice",
    "Mindfulness Moment",
    "Daily Routine",
]

CONTENT_TEMPLATES = [
    "Today was {mood_desc}. I spent time {activity} and it made me feel {emotion}. {reflection}",
    "Had an interesting day {activity}. The weather was {weather} which {weather_effect}. {personal_note}",
    "Woke up feeling {emotion} today. Decided to {activity} which turned out {outcome}. {learning}",
    "Reflecting on {topic} today. It's amazing how {observation}. {future_plan}",
    "Spent quality time {activity} today. These moments remind me of {memory}. {gratitude}",
]

ACTIVITIES = [
    "reading a fascinating book", "cooking a new recipe", "going for a long walk", "meeting with friends",
    "working on a creative project", "organizing my space", "learning a new skill", "exercising",
    "gardening", "listening to music", "watching documentaries", "writing in my journal",
    "exploring the city", "having deep conversations", "practicing mindfulness", "planning future goals"
]

EMOTIONS = [
    "grateful", "inspired", "peaceful", "energetic", "contemplative", "joyful", "motivated",
    "relaxed", "curious", "optimistic", "reflective", "content", "excited", "serene"
]

MOODS = ["happy", "calm", "excited", "reflective", "grateful", "peaceful", "energetic"]

TAGS_POOL = [
    "family", "friends", "work", "travel", "food", "exercise", "creativity", "learning",
    "nature", "technology", "books", "music", "goals", "health", "mindfulness", "growth",
    "memories", "gratitude", "adventure", "home", "weekend", "morning", "evening"
]

WEATHER = ["sunny", "rainy", "cloudy", "beautiful", "crisp", "warm"]
WEATHER_EFFECTS = [
    "made me want to stay indoors", "inspired me to go outside", "created a cozy atmosphere",
    "energized my mood", "made everything feel fresh", "brought a sense of calm"
]

REFLECTIONS = [
    "Sometimes the smallest moments bring the greatest joy.",
    "I'm learning to appreciate the present moment more each day.",
    "Life has a way of surprising us when we least expect it.",
    "Growth happens in the quiet moments between the chaos.",
    "Every day offers a new opportunity to learn something about myself."
]

def create_sample_entries():
    """Create sample diary entries spanning different time periods."""
    
    # Get all users and let user choose
    users = User.objects.all()
    if not users:
        print("❌ No users found. Please create a user account first.")
        return
    
    print("👥 Available users:")
    for i, user in enumerate(users, 1):
        entry_count = Entry.objects.filter(author=user).count()
        print(f"   {i}. {user.username} (currently has {entry_count} entries)")
    
    # Let user choose which account to populate
    while True:
        try:
            choice = input(f"\n🎯 Which user account should get the sample entries? (1-{len(users)} or 'all'): ").strip().lower()
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
        print(f"\n🌱 Creating sample entries for user: {user.username}")
        
        # Check existing entries
        existing_count = Entry.objects.filter(author=user).count()
        if existing_count > 0:
            response = input(f"⚠️  Found {existing_count} existing entries for {user.username}. Delete them? (y/N): ")
            if response.lower() == 'y':
                Entry.objects.filter(author=user).delete()
                print("🗑️  Existing entries deleted.")

        entries_created = 0
        
        # Create entries spanning different time periods
        today = datetime.now().date()
        
        # 1. Recent entries (last 30 days) - these will be active
        print("📝 Creating recent entries (last 30 days)...")
        for i in range(15):
            entry_date = today - timedelta(days=randint(0, 30))
            create_entry(user, entry_date, is_recent=True)
            entries_created += 1
        
        # 2. Older entries (3-6 months ago) - these will be eligible for archive  
        print("📚 Creating older entries (3-6 months ago)...")
        for i in range(20):
            entry_date = today - timedelta(days=randint(90, 180))
            create_entry(user, entry_date, is_recent=False)
            entries_created += 1
        
        # 3. Very old entries (6+ months ago) - these will be auto-eligible for archive
        print("🗄️  Creating very old entries (6+ months ago)...")
        for i in range(25):
            entry_date = today - timedelta(days=randint(180, 400))
            create_entry(user, entry_date, is_recent=False, is_very_old=True)
            entries_created += 1
        
        # 4. Create some entries from different years
        print("📅 Creating entries from previous years...")
        for year_offset in [1, 2]:
            for i in range(10):
                entry_date = today.replace(year=today.year - year_offset) - timedelta(days=randint(0, 365))
                create_entry(user, entry_date, is_recent=False, is_very_old=True)
                entries_created += 1
        
        print(f"✅ Created {entries_created} sample diary entries for {user.username}!")
    
    # Final summary
    total_entries = Entry.objects.count()
    print(f"\n📊 Final database summary:")
    print(f"   • Total entries in database: {total_entries}")
    for user in User.objects.all():
        user_entries = Entry.objects.filter(author=user).count()
        archived_count = Entry.objects.filter(author=user, is_archived=True).count()
        print(f"   • {user.username}: {user_entries} entries ({archived_count} archived)")
    
    print(f"\n🎯 Now you can test:")
    print(f"   • Archive dashboard: See statistics and eligible entries")
    print(f"   • Bulk archive: Archive entries older than 6 months")
    print(f"   • Search functionality: Find entries by date, mood, tags")
    print(f"   • Archive/restore: Toggle individual entry archive status")

def create_entry(user, entry_date, is_recent=True, is_very_old=False):
    """Create a single diary entry with realistic content."""
    
    title = choice(TITLES)
    mood = choice(MOODS)
    
    # Generate content
    template = choice(CONTENT_TEMPLATES)
    activity = choice(ACTIVITIES)
    emotion = choice(EMOTIONS)
    weather = choice(WEATHER)
    weather_effect = choice(WEATHER_EFFECTS)
    reflection = choice(REFLECTIONS)
    
    mood_descriptions = {
        "happy": "wonderful", "calm": "peaceful", "excited": "energetic",
        "reflective": "thoughtful", "grateful": "blessed", "peaceful": "serene",
        "energetic": "dynamic"
    }
    
    content = template.format(
        mood_desc=mood_descriptions.get(mood, "interesting"),
        activity=activity,
        emotion=emotion,
        weather=weather,
        weather_effect=weather_effect,
        reflection=reflection,
        observation="perspective shapes our reality",
        topic="life's unexpected turns",
        outcome="better than expected",
        learning="I learned something valuable about patience today.",
        memory="the importance of being present",
        gratitude="I'm grateful for these simple pleasures.",
        personal_note="Looking forward to more days like this.",
        future_plan="Tomorrow I want to try something new."
    )
    
    # Add some variety to content length
    if randint(1, 3) == 1:
        content += f"\n\n{choice(REFLECTIONS)} The little things in life often matter the most."
    
    # Select random tags
    num_tags = randint(2, 5)
    tags = ", ".join(choice(TAGS_POOL) for _ in range(num_tags))
    
    # Create the entry
    entry = Entry.objects.create(
        author=user,
        title=title,
        content=content,
        date=entry_date,
        mood=mood,
        tags=tags,
        is_private=choice([True, False]) if randint(1, 4) == 1 else False,  # 25% chance of private
    )
    
    # For very old entries, only a few might already be archived (to test restore functionality)
    if is_very_old and randint(1, 10) == 1:  # 10% chance - most entries will be unarchived for testing
        entry.archive()
    
    return entry

if __name__ == "__main__":
    print("🌱 Diary Seed Script")
    print("=" * 50)
    create_sample_entries()
