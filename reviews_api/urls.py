"""
URL configuration for reviews_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from reviews import views as review_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth
    path("api/auth/register/", review_views.RegisterView.as_view(), name="register"),
    path("api/auth/login/", review_views.LoginView.as_view(), name="login"),
    # Reviews
    path("api/reviews/add/", review_views.AddReviewView.as_view(), name="add-review"),
    # Places search & detail
    path("api/places/search/", review_views.SearchPlacesView.as_view(), name="search-places"),
    path("api/places/<int:pk>/", review_views.PlaceDetailView.as_view(), name="place-detail"),
]
