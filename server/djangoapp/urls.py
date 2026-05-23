from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path("registration", views.registration, name="registration"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_request, name="logout"),

    # CARS
    path("get_cars", views.get_cars, name="get_cars"),

    # DEALERSHIPS
   path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),

    # DEALER DETAILS + REVIEWS
    path("dealer/<int:dealer_id>", views.get_dealer_details, name="dealer_details"),
    path("dealer/<int:dealer_id>/reviews", views.get_dealer_reviews, name="dealer_reviews"),

    # ADD REVIEW
    path("add_review", views.add_review, name="add_review"),
        path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
