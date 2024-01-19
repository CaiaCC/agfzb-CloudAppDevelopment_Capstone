from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime, date
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://caiachuang-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://caiachuang-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealer's reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["review_list"] = reviews
        context["dealer_id"] = dealer_id

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://caiachuang-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealer = get_dealer_by_id_from_cf(url, dealer_id)
        context["dealer_name"] = dealer["full_name"]

        context["cars"] = CarModel.objects.filter(dealer_id=dealer_id)
        for car in context["cars"]:
            print("CAR", car)
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        url = "https://caiachuang-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        # only authenticated users can post reviews for a dealer
        if (request.user.is_authenticated):
            data = request.POST
            review = {}
            has_purchased = "purchasecheck" in data
            name = f"{request.user.first_name} {request.user.last_name}"
            if (name == " "):
                name = request.user.username
            if has_purchased:
                car = CarModel.objects.get(pk=data["car"])
                review["car_make"] = car.car_make.name
                review["car_model"] = car.name
                review["car_year"]= car.year.strftime("%Y")
            else:
                review["car_make"] = None
                review["car_model"] = None
                review["car_year"]= None
            review["id"] = 0
            review["name"] = name
            review["dealership"] = dealer_id
            review["review"] = data["content"]
            review["purchase"] = has_purchased
            review["purchase_date"] = data["purchasedate"]

            try:
                response = post_request(url, review, dealer_id=dealer_id)
            except Exception as error:
                print("Post Review Error:", error)
            
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
