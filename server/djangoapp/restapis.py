import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    json_data = {}
    try:
        if 'apikey' in kwargs:
            # Basic authentication GET
            requests.get(url, data=kwargs, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', kwargs['api_key']))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except Exception as error:
        print("Network exception occurred", error)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
    results = []
    # Call get_request with URL and dealerId parameter
    json_result = get_request(url, id=dealerId)
    print("get_dealer_reviews_from_cf", json_result)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a DealerView object with values in `doc` object
            review_obj = DealerReview(
                        dealership=review_doc["dealership"],
                        name=review_doc["name"],
                        purchase=review_doc["purchase"],
                        review=review_doc["review"],
                        purchase_date=review_doc["purchase_date"],
                        car_make=review_doc["car_make"],
                        car_model=review_doc["car_model"],
                        car_year=review_doc["car_year"],
                        sentiment=analyze_review_sentiments(review_doc["review"]),
                        id=review_doc["id"])
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    return "HELLO"
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



