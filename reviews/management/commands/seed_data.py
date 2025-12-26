import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from reviews.models import Place, Review, User


class Command(BaseCommand):
    help = "Populate the database with sample users, places, and reviews."

    def handle(self, *args, **options):
        random.seed(42)

        users = []
        for i in range(10):
            phone = f"900000000{i}"
            user, created = User.objects.get_or_create(
                phone=phone,
                defaults={"name": f"User {i}", "password": "password123"},
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        place_specs = [
            ("Star Cafe", "MG Road, Bangalore", "restaurant"),
            ("Health Plus Clinic", "Indiranagar, Bangalore", "doctor"),
            ("Book World", "Brigade Road, Bangalore", "shop"),
            ("Daily Mart", "HSR Layout, Bangalore", "shop"),
            ("Tasty Bites", "Koramangala, Bangalore", "restaurant"),
        ]

        places = []
        for name, address, category in place_specs:
            place, _ = Place.objects.get_or_create(
                name=name,
                address=address,
                defaults={"category": category},
            )
            places.append(place)

        review_texts = [
            "Great service and friendly staff.",
            "Average experience, could be better.",
            "Loved it! Highly recommend.",
            "Not satisfied with the quality.",
            "Good value for money.",
        ]

        for place in places:
            for user in users:
                if random.random() < 0.7:
                    rating = random.randint(1, 5)
                    text = random.choice(review_texts)
                    days_ago = random.randint(0, 60)
                    review, created = Review.objects.get_or_create(
                        place=place,
                        user=user,
                        defaults={
                            "rating": rating,
                            "text": text,
                        },
                    )
                    # Update created_at to simulate older reviews
                    if days_ago > 0:
                        review.created_at = timezone.now() - timedelta(days=days_ago)
                        review.save(update_fields=["created_at"])

        self.stdout.write(self.style.SUCCESS("Sample data populated successfully."))


