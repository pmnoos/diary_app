from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from entries.models import Entry
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create demo user and sample diary entries for demonstration purposes'

    def handle(self, *args, **options):
        # Create or get demo user
        demo_user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User',
            }
        )
        
        if created:
            demo_user.set_password('demo_password_123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user account'))
        else:
            self.stdout.write('Demo user already exists')

        # Create sample entries if they don't exist
        existing_entries = Entry.objects.filter(author=demo_user).count()
        
        if existing_entries == 0:
            # Sample entries with realistic content
            sample_entries = [
                {
                    'title': 'My First Day at the New Job',
                    'content': '''Today was my first day at the new company and I'm feeling excited but also a bit nervous! 

The office has a really nice atmosphere and everyone seems friendly. My manager Sarah gave me a tour of the facilities and introduced me to the team. The workspace is modern with lots of natural light, which I really appreciate.

I spent most of the day setting up my computer and going through orientation materials. There's definitely a lot to learn, but I'm looking forward to the challenge. The company culture seems very collaborative and innovative.

Tomorrow I'll start working on my first project with the development team. Can't wait to dive in and start contributing!

Check out the company website: https://example.com - they have some really interesting projects showcased there.''',
                    'created_at': timezone.now() - timedelta(days=5)
                },
                {
                    'title': 'Weekend Hiking Adventure',
                    'content': '''What an amazing weekend! Went hiking with friends at the national park and the views were absolutely breathtaking.

We started early in the morning around 6 AM to beat the crowds. The trail was challenging but so worth it - we climbed about 1,200 feet in elevation over 4 miles. The weather was perfect with clear skies and a gentle breeze.

At the summit, we had a fantastic view of the valley below and the mountain ranges in the distance. We spent about an hour at the top, eating lunch and taking photos. Nature really has a way of putting things in perspective.

My fitness tracker showed we burned over 800 calories! My legs are definitely feeling it today, but I'm already planning our next adventure.

Here's a link to the trail guide we used: https://trailguide.example.com - highly recommend it for anyone looking for a moderate challenge.''',
                    'created_at': timezone.now() - timedelta(days=3)
                },
                {
                    'title': 'Learning Python - Progress Update',
                    'content': '''Been working through a Python programming course for the past month and I'm starting to feel more confident with the language!

Today I completed a project that scrapes data from a website and generates a simple report. It's incredible how much you can accomplish with just a few lines of Python code. The project involved:

- Web scraping with BeautifulSoup
- Data processing with pandas
- Creating visualizations with matplotlib

The most challenging part was handling different data formats and cleaning up messy data. But that's probably what makes programming so satisfying - solving complex problems step by step.

I'm planning to build a personal project next - maybe a simple web app using Django. The course instructor mentioned it's a great framework for beginners.

Resources I've been using:
- Python documentation: https://docs.python.org
- Helpful tutorials: https://realpython.com

Excited to see where this journey takes me!''',
                    'created_at': timezone.now() - timedelta(days=2)
                },
                {
                    'title': 'Rainy Day Reflections',
                    'content': '''It's been raining all day today, which gave me a perfect excuse to stay indoors and catch up on some reading.

There's something really peaceful about the sound of rain against the windows. I made myself a cup of tea, wrapped up in a cozy blanket, and dove into that book I've been meaning to finish for weeks.

The book is about personal growth and mindfulness - really making me think about being more present in daily life. It's easy to get caught up in the hustle and bustle and forget to appreciate the simple moments.

I also spent some time organizing my photos from recent trips. It's fun to look back at all the memories and adventures from this year. I should really print some of these and create a proper photo album.

Sometimes slow, quiet days like this are exactly what we need to recharge and reflect. Tomorrow will bring new adventures, but today is for rest and contemplation.''',
                    'created_at': timezone.now() - timedelta(days=1)
                },
                {
                    'title': 'Cooking Experiment: Homemade Pizza',
                    'content': '''Decided to try making pizza from scratch today and it turned out better than expected!

I've been wanting to experiment more in the kitchen, so I found a recipe online for homemade pizza dough. The process was actually quite therapeutic - kneading the dough by hand was surprisingly relaxing.

For toppings, I went with a classic margherita style: fresh mozzarella, tomato sauce, basil, and a drizzle of olive oil. Simple but delicious. The crust came out crispy on the bottom and perfectly chewy in the middle.

The whole process took about 3 hours from start to finish (including dough rising time), but it was so worth it. Nothing beats the satisfaction of eating something you made entirely from scratch.

Next time I want to try a BBQ chicken pizza or maybe a Mediterranean style with olives and feta cheese. 

Here's the recipe I followed: https://cookingbasics.example.com/pizza-dough

Definitely adding this to my regular cooking rotation!''',
                    'created_at': timezone.now()
                }
            ]

            for entry_data in sample_entries:
                Entry.objects.create(
                    title=entry_data['title'],
                    content=entry_data['content'],
                    author=demo_user,
                    created_at=entry_data['created_at'],
                    updated_at=entry_data['created_at']
                )

            self.stdout.write(
                self.style.SUCCESS(f'Created {len(sample_entries)} demo entries')
            )
        else:
            self.stdout.write(f'Demo user already has {existing_entries} entries')

        self.stdout.write(
            self.style.SUCCESS('Demo setup complete! Demo entries are now available.')
        )
