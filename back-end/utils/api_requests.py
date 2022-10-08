
"""API Request handling
"""

import time
import requests
from ratelimit import limits, sleep_and_retry

MAX_RETRIES = 5

# TODO make more robust with retries etc.
def get_request(url, headers, params=None, timeout=5, retry_count=0):
    """Method to catch connection errors
    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout, params=params)
    except TimeoutError:
        # if timeout then stop trying
        response = None
    except:
        if retry_count == MAX_RETRIES:
            print(f"Max retries exceeded for {url}")
            response = None
        else:
            print(f"Retrying {url}, count {retry_count}")
            time.sleep(1)
            response = get_request(url, headers, params, timeout, retry_count + 1)
    return response


def post_request(url, headers, payload, timeout=10, retry_count=0):
    """Method to catch connection errors
    """
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=timeout)
    except TimeoutError:
        # if timeout then stop trying
        print("API request timeout, retry with larger timeout")
        response = None
    except:
        if retry_count == MAX_RETRIES:
            print(f"Max retries exceeded for {url}")
            response = None
        else:
            time.sleep(2)
            response = post_request(url, headers, payload, timeout, retry_count + 1)
    return response
