import requests

def is_url_reachable(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


import time

def retrieve_phone_code(phone_number):
    """
    Simulate retrieving SMS code for the given phone number.
    In production, this might fetch the code from an API or test DB.
    """
    # Simulate delay and return a dummy code
    time.sleep(1)
    return "1234"
