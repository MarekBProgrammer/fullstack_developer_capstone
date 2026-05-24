from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path("registration", views.registration, name="registration"),
    path("login_user", views.login_user, name="login"),
    path("logout_request", views.logout_request, name="logout"),

    # CARS
    path("get_cars", views.get_cars, name="get_cars"),

    # DEALERSHIPS
    path("get_dealerships", views.get_dealerships, name="get_dealerships"),
    path("get_dealerships/<str:state>", views.get_dealerships, name="get_dealerships_by_state"),

    # DEALER DETAILS + REVIEWS
    path("dealer/<int:dealer_id>", views.get_dealer_details, name="dealer_details"),
    path("dealer/<int:dealer_id>/reviews", views.get_dealer_reviews, name="dealer_reviews"),

    # ADD REVIEW
    path("add_review", views.add_review, name="add_review"),

    # REVIEWS BY DEALER
    path("reviews/dealer/<int:dealer_id>", views.get_dealer_reviews, name="dealer_reviews_by_id"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
