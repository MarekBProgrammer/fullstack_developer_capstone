from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import logging

from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


# LOGIN
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "status": "Failed"})

    return JsonResponse({"status": "Invalid request"})


# LOGOUT
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


# REGISTRATION
@csrf_exempt
def registration(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"status": "Invalid request"})


# GET CARS (dropdown)
def get_cars(request):
    if request.method == "GET":
        carmodels = [
            {"CarMake": "NISSAN", "CarModel": "XTRAIL"},
            {"CarMake": "BMW", "CarModel": "X5"},
            {"CarMake": "TOYOTA", "CarModel": "COROLLA"},
            {"CarMake": "HONDA", "CarModel": "CIVIC"},
        ]
        return JsonResponse({"CarModels": carmodels})


# GET DEALERSHIPS
def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# GET DEALER REVIEWS
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review in reviews:
            text = review.get("review", "")
            review["sentiment"] = analyze_review_sentiments(text)

        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# GET DEALER DETAILS
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# ADD REVIEW (POST)
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = post_review(data)
        return JsonResponse({"status": 200, "result": result})

    return JsonResponse({"status": 400, "message": "Invalid request"})
