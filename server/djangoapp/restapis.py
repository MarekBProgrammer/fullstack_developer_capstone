# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        params = "&".join([f"{k}={v}" for k, v in kwargs.items()])

    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params

    print("GET from {} ".format(request_url))

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return []  # <-- KLUCZOWE


# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments
def analyze_review_sentiments(text):
    try:
        request_url = sentiment_analyzer_url + "analyze/" + text
        response = requests.get(request_url)
        result = response.json()
        return result.get("sentiment", "neutral")
    except:
        return "neutral"


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")

