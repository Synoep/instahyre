from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, name, password=None, **extra_fields):
        if not phone:
            raise ValueError("Users must have a phone number")
        phone = self.normalize_email(phone) if "@" in phone else phone
        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses phone number as the unique identifier.

    Assumption: We store a password even though the product requirement
    only mentions name and phone, to have a secure login mechanism.
    """

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Place(models.Model):
    CATEGORY_CHOICES = [
        ("shop", "Shop"),
        ("doctor", "Doctor"),
        ("restaurant", "Restaurant"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other", blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "address"],
                name="unique_place_name_address",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.address[:50]}"


class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("reviews.User", on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["place", "-created_at"]),
        ]

    def __str__(self):
        return f"Review {self.rating} by {self.user} on {self.place}"
