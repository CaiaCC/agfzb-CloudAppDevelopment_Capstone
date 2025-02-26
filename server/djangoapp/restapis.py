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
            response = requests.get(url, data=kwargs, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', kwargs['apikey']))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code
        print("GET With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except Exception as error:
        print("Get Request exception occurred", error)
    return json_data


def post_request(url, json_payload, **kwargs):
    json_data = {}
    print(kwargs)
    print("Post from {} ".format(url))

    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        json_data = json.loads(response.text)
        status_code = response.status_code
        print("POST With status {} ".format(status_code))

    except Exception as error:
        print("Post Request exception occurred", error)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        print(json_result)
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(url, dealerId):
    json_result = get_request(url, id=dealerId)

    if json_result:
        return json_result[0]
    else:
        return {}


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with URL and dealerId parameter
    json_result = get_request(url, id=dealerId)
    # print("get_dealer_reviews_from_cf", json_result)
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
                            id=review_doc["id"],
                        )
            results.append(review_obj)

    return results


def analyze_review_sentiments(review):
    NLU_API_KEY = "vw87ZFFr3Odo0UAxRWaS0dCsHdLXxQHvBHcGJBeXOMEq"
    NLU_URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/f023178b-ec56-4ae4-8e5d-de4d6208f6a8/v1/analyze?version=2022-04-07'
    # features = ["sentiment"]
    # analysis = get_request(NLU_URL, apikey=NLU_API_KEY, features=features, text=review)
    params = json.dumps({"text": review, "features": {"sentiment": {}}})
    response = requests.post(NLU_URL, data=params, headers={'Content-Type':'application/json'}, auth=HTTPBasicAuth("apikey", NLU_API_KEY))

    try:
        label = response.json()['sentiment']['document']['label']
        return label
    except Exception as error:
        print("Analyze Sentiments Exception Occur:", error)
        return 'neutral'


