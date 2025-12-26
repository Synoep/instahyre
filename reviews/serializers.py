from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Place, Review, User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "name", "phone", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("Invalid phone or password.")
        attrs["user"] = user
        return attrs


class PlaceSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ["id", "name", "address", "category", "average_rating"]
    
    def get_average_rating(self, obj):
        return obj.average_rating if obj.average_rating is not None else 0.0


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "rating", "text", "user_name", "created_at"]


class PlaceDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = ["id", "name", "address", "category", "average_rating", "reviews"]
    
    def get_average_rating(self, obj):
        return obj.average_rating if obj.average_rating is not None else 0.0


class AddReviewSerializer(serializers.Serializer):
    place_name = serializers.CharField()
    place_address = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(allow_blank=True, required=False)
    category = serializers.ChoiceField(
        choices=Place.CATEGORY_CHOICES, required=False, allow_blank=True
    )


