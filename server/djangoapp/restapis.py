import requests
import json

from requests.auth import HTTPBasicAuth
from .models import CarDealer, CarMake, CarModel, DealerReview

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    url =  "http://127.0.0.1:5000/api/post_review"
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(json_result)
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

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    # print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc.get("short_name"))
    return dealer_obj

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_reviews_from_cf(url, dealer_id):
#     results = []
#     # Perform a GET request with the specified dealer id
#     json_result = get_request(url, dealerId=dealer_id)

#     if json_result:
#         # Get all review data from the response
#         reviews = json_result["body"]["data"]["docs"]
#         # For every review in the response
#         for review in reviews:
#             # Create a DealerReview object from the data
#             # These values must be present
#             review_content = review["review"]
#             id = review["_id"]
#             name = review["name"]
#             purchase = review["purchase"]
#             dealership = review["dealership"]

#             try:
#                 # These values may be missing
#                 car_make = review["car_make"]
#                 car_model = review["car_model"]
#                 car_year = review["car_year"]
#                 purchase_date = review["purchase_date"]

#                 # Creating a review object
#                 review_obj = DealerReview(dealership=dealership, id=id, name=name, 
#                                           purchase=purchase, review=review_content, car_make=car_make, 
#                                           car_model=car_model, car_year=car_year, purchase_date=purchase_date
#                                           )

#             except KeyError:
#                 print("Something is missing from this review. Using default values.")
#                 # Creating a review object with some default values
#                 review_obj = DealerReview(
#                     dealership=dealership, id=id, name=name, purchase=purchase, review=review_content)

#             # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
#             review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             print(f"sentiment: {review_obj.sentiment}")

#             # Saving the review object to the list of results
#             results.append(review_obj)

#     return results

# def get_dealer_reviews_by_id_from_cf(url, dealer_id):
#     results = []
#     json_result = get_request(url, dealerId=dealer_id)
#     if json_result:
#         data = json_result['data']
#         reviews = data['docs']
#         for review in reviews:
#             #review = reviewx["docs"]
#             try:
#                 review_obj = DealerReview(name = review["name"], 
#                 dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
#                 purchase_date = review["purchase_date"], car_make = review['car_make'],
#                 car_model = review['car_model'], car_year= review['car_year'], sentiment= "none")
#             except:
#                 review_obj = DealerReview(name = review["name"], 
#                 dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
#                 purchase_date = 'none', car_make = 'none',
#                 car_model = 'none', car_year= 'none', sentiment= "none")
                
#             #review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             #print(review_obj.sentiment)
                    
#             results.append(review_obj)

#     return results


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    print(json_result, "96")
    if json_result:
        if isinstance(json_result, list):  # Check if json_result is a list
            reviews = json_result
        else:
            reviews = json_result["data"]["docs"]

        # Check if 'reviews' is a list of one dictionary
        if isinstance(reviews, list) and len(reviews) == 1 and isinstance(reviews[0], dict):
            reviews = reviews[0]

        for dealer_review in reviews:
            print("dealer_review--------------------", dealer_review)  # Print dealer_review
            if isinstance(dealer_review, str):  # Check if dealer_review is a string
                try:
                    dealer_review = json.loads(dealer_review)
                except json.JSONDecodeError:
                    continue  # Skip this iteration if the JSON decoding fails

            review_obj = DealerReview(
                dealership=dealer_review.get("dealership"),
                name=dealer_review.get("name"),
                purchase=dealer_review.get("purchase"),
                review=dealer_review.get("review"),
                purchase_date=dealer_review.get("purchase_date"),
                car_make=dealer_review.get("car_make"),
                car_model=dealer_review.get("car_model"),
                car_year=dealer_review.get("car_year"),
                sentiment='',
                id=dealer_review.get("id")
            )

            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results
    
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/b7caac7c-51a7-4fdc-a97a-1c08bd26b270"
    api_key = "Q6Jf0YRogH0B1rA4QpB0_7_awUAKrft_WxXFb7tQH722"
    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

    natural_language_understanding.set_service_url(url) 

    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result() 

    label=json.dumps(response, indent=2) 

    label = response['sentiment']['document']['label'] 

    return(label) 