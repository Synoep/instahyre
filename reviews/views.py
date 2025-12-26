from django.db.models import Avg, Case, IntegerField, Q, When
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Place, Review
from .serializers import (
    AddReviewSerializer,
    LoginSerializer,
    PlaceDetailSerializer,
    PlaceSerializer,
    ReviewSerializer,
    UserRegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class AddReviewView(APIView):
    """
    Add a review by providing place name, address and rating.
    Creates the place if it does not already exist.
    """

    def post(self, request):
        serializer = AddReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        place, created = Place.objects.get_or_create(
            name=data["place_name"].strip(),
            address=data["place_address"].strip(),
            defaults={
                "category": data.get("category") or "other",
            },
        )

        review = Review.objects.create(
            place=place,
            user=request.user,
            rating=data["rating"],
            text=data.get("text", ""),
        )

        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class SearchPlacesView(generics.ListAPIView):
    serializer_class = PlaceSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        min_rating = self.request.query_params.get("min_rating")
        category = self.request.query_params.get("category")

        queryset = Place.objects.all().annotate(
            average_rating=Avg("reviews__rating")
        )

        if min_rating is not None:
            try:
                min_rating_val = float(min_rating)
                # Filter by min_rating, excluding places with no reviews (None average_rating)
                queryset = queryset.filter(average_rating__gte=min_rating_val).exclude(average_rating__isnull=True)
            except ValueError:
                pass

        if category:
            queryset = queryset.filter(category__iexact=category)

        if name:
            name = name.strip()
            queryset = queryset.filter(name__icontains=name).annotate(
                exact_match=Case(
                    When(Q(name__iexact=name), then=1),
                    default=0,
                    output_field=IntegerField(),
                )
            ).order_by("-exact_match", "name")
        else:
            queryset = queryset.order_by("name")

        return queryset


class PlaceDetailView(generics.RetrieveAPIView):
    queryset = Place.objects.all().annotate(average_rating=Avg("reviews__rating"))
    serializer_class = PlaceDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Order reviews: current user's review first (if exists), then newest first
        user_review_q = instance.reviews.filter(user=request.user)
        other_reviews_q = instance.reviews.exclude(user=request.user)

        ordered_reviews = list(user_review_q.order_by("-created_at")) + list(
            other_reviews_q.order_by("-created_at")
        )

        place_data = PlaceDetailSerializer(instance).data
        place_data["reviews"] = ReviewSerializer(ordered_reviews, many=True).data
        return Response(place_data)
