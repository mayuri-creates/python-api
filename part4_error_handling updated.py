"""
Part 4: Robust Error Handling
=============================
Difficulty: Intermediate+

Learn:
- Try/except blocks for API requests
- Handling network errors
- Timeout handling
- Response validation
"""

import requests
import time
import logging
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException

logging.basicConfig(level=logging.INFO)


def safe_api_request(url, timeout=5):
    try:
        logging.info(f"Calling API: {url}")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return {"success": True, "data": response.json()}

    except ConnectionError:
        return {"success": False, "error": "Internet connection problem"}

    except Timeout:
        return {"success": False, "error": "Request timed out"}

    except HTTPError as e:
        return {"success": False, "error": f"HTTP error {e.response.status_code}"}

    except RequestException:
        return {"success": False, "error": "Request failed"}


# -------------------------------
# Exercise 1: Retry Logic
# -------------------------------

def safe_request_with_retry(url, retries=3):
    for attempt in range(1, retries + 1):
        print(f"Attempt {attempt}")
        result = safe_api_request(url)

        if result["success"]:
            return result

        print("Retrying...")
        time.sleep(1)

    return {"success": False, "error": "Failed after retries"}



# Exercise 2: Validate Crypto Data


def validate_crypto_data(data):
    if "quotes" in data and "USD" in data["quotes"]:
        return True
    return False


def fetch_crypto_safely():
    print("\nCrypto Price Checker\n")

    coin = input("Enter coin (btc-bitcoin / eth-ethereum): ").strip().lower()
    url = f"https://api.coinpaprika.com/v1/tickers/{coin}"

    result = safe_request_with_retry(url)

    if result["success"]:
        data = result["data"]

        if validate_crypto_data(data):
            print("Coin:", data["name"])
            print("Price:", round(data["quotes"]["USD"]["price"], 2))
        else:
            print("Invalid crypto data format")
    else:
        print(result["error"])



# Exercise 3: Logging Example


def demo_error_handling():
    print("\nError Handling Demo\n")

    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/99999",
        "https://wrong-url-test.com"
    ]

    for url in urls:
        result = safe_api_request(url)
        if result["success"]:
            print("Success:", url)
        else:
            print("Error:", result["error"])


def main():
    demo_error_handling()
    fetch_crypto_safely()


if __name__ == "__main__":
    main()



# --- EXERCISES ---
#
# Exercise 1: Add retry logic - if request fails, try again up to 3 times
#             Hint: Use a for loop and time.sleep() between retries
#
# Exercise 2: Create a function that validates crypto response
#             Check that 'quotes' and 'USD' keys exist before accessing
#
# Exercise 3: Add logging to track all API requests
#             import logging
#             logging.basicConfig(level=logging.INFO)
