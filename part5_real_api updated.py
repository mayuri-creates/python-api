"""
Part 5: Real-World APIs - Weather & Crypto Dashboard
====================================================
Difficulty: Advanced

Learn:
- Working with multiple real APIs
- Data formatting and presentation
- Building a simple CLI dashboard
- Using environment variables for API keys (optional)
"""

import requests
import json
import os
from datetime import datetime, timedelta

#  CITY & CRYPTO DATA 
CITIES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "sydney": (-33.8688, 151.2093),
    "paris": (48.8566, 2.3522),
    "berlin": (52.5200, 13.4050)
}

CRYPTO_IDS = {
    "bitcoin": "btc-bitcoin",
    "ethereum": "eth-ethereum",
    "dogecoin": "doge-dogecoin",
    "cardano": "ada-cardano",
    "solana": "sol-solana",
    "ripple": "xrp-xrp"
}

# WEATHER FUNCTIONS 
def get_weather(city):
    city = city.lower().strip()
    if city not in CITIES:
        print(f"City '{city}' not found. Available: {', '.join(CITIES.keys())}")
        return None
    lat, lon = CITIES[city]
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {"latitude": lat, "longitude": lon, "current_weather": True, "timezone": "auto"}
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        print(f"Weather fetch error: {e}")
        return None

def show_weather(city):
    data = get_weather(city)
    if not data: return
    current = data["current_weather"]
    print(f"\nWeather in {city.title()}:")
    print(f"Temperature: {current['temperature']}°C")
    print(f"Wind Speed: {current['windspeed']} km/h")
    print(f"Wind Direction: {current['winddirection']}°")

# CRYPTO FUNCTIONS
def get_crypto_price(coin):
    coin_id = CRYPTO_IDS.get(coin.lower(), coin.lower())
    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        print(f"Crypto fetch error: {e}")
        return None

def show_crypto(coin):
    data = get_crypto_price(coin)
    if not data:
        print(f"Coin '{coin}' not found.")
        return
    usd = data["quotes"]["USD"]
    print(f"\n{data['name']} ({data['symbol']})")
    print(f"Price: ${usd['price']:.2f}, Market Cap: ${usd['market_cap']:.0f}")
    print(f"24h Change: {usd['percent_change_24h']:+.2f}%")

def compare_cryptos(coins):
    print("\nCrypto Comparison Table")
    print(f"{'Name':<15}{'Price':<15}{'24h Change'}")
    print("-"*40)
    for coin in coins:
        data = get_crypto_price(coin)
        if data:
            usd = data["quotes"]["USD"]
            print(f"{data['name']:<15}${usd['price']:<14.2f}{usd['percent_change_24h']:+.2f}%")

# POST & SAVE 
def make_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {"title": "My Post", "body": "This is content", "userId": 1}
    try:
        res = requests.post(url, json=payload, timeout=5)
        print("\nPOST Response:")
        print(res.json())
    except requests.RequestException as e:
        print(f"POST error: {e}")

def save_to_file(data, filename="results.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved results to {filename}")

#  OPENWEATHERMAP 
def get_weather_openweathermap(city):
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        print("No OpenWeatherMap API key found in environment variables.")
        return
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        print(f"\nOpenWeatherMap - {city.title()}: {data['main']['temp']}°C, {data['weather'][0]['description']}")
    except requests.RequestException as e:
        print(f"Error: {e}")

# OMDB API 
def get_movie_info():
    api_key = "dbe12aae"

    movie = input("Enter movie title: ").strip()
    url = f"http://www.omdbapi.com/?t={movie}&apikey={api_key}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        if data.get("Response") == "True":
            print(f"\nTitle: {data['Title']}")
            print(f"Year: {data['Year']}")
            print(f"Genre: {data['Genre']}")
            print(f"Director: {data['Director']}")
            print(f"IMDB Rating: {data['imdbRating']}")
            print(f"Plot: {data['Plot']}")
        else:
            print("Movie not found!")
    except requests.RequestException as e:
        print(f"OMDB API error: {e}")

# AQI LAST 7 DAYS 
def get_aqi():
    city = input("Enter city for AQI (PM2.5) data: ").strip().lower()
    if city not in CITIES:
        print("City not found.")
        return

    lat, lon = CITIES[city]
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": "pm2_5"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        print(f"\nPM2.5 Levels in {city.title()} (last 7 days):")
        for time, value in zip(data["hourly"]["time"], data["hourly"]["pm2_5"]):
            print(f"{time}: {value} µg/m³")

    except requests.RequestException as e:
        print(f"AQI fetch error: {e}")


# DASHBOARD MENU 
def dashboard():
    while True:
        print("\n--- MENU ---")
        print("1. Weather")
        print("2. Crypto Price")
        print("3. Compare Cryptos")
        print("4. POST Example")
        print("5. Save Sample JSON")
        print("6. OpenWeatherMap")
        print("7. OMDB Movie Info")
        print("8. Last 7 Days AQI")
        print("9. Exit")
        choice = input("Choose option: ").strip()
        if choice == "1":
            city = input("Enter city: ")
            show_weather(city)
        elif choice == "2":
            coin = input("Enter coin: ")
            show_crypto(coin)
        elif choice == "3":
            coins = input("Enter coins comma separated: ").split(",")
            compare_cryptos([c.strip() for c in coins])
        elif choice == "4":
            make_post()
        elif choice == "5":
            save_to_file({"weather": "sunny", "crypto": "bitcoin"})
        elif choice == "6":
            city = input("Enter city for OpenWeatherMap: ")
            get_weather_openweathermap(city)
        elif choice == "7":
            get_movie_info()
        elif choice == "8":
            get_aqi()
        elif choice == "9":
            print("Exiting. Thank you")
            break
        else:
            print("Invalid option. Try again.")

# RUN DASHBOARD 
if __name__ == "__main__":
    print(f"Enhanced API Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    dashboard()



# --- CHALLENGE EXERCISES ---
#
# Exercise 1: Add more cities to the CITIES dictionary
#             Find coordinates at: https://www.latlong.net/
#
# Exercise 2: Create a function that compares prices of multiple cryptos
#             Display them in a formatted table
#
# Exercise 3: Add POST request example
#             Use: https://jsonplaceholder.typicode.com/posts
#             Send: requests.post(url, json={"title": "My Post", "body": "Content"})
#
# Exercise 4: Save results to a JSON file
#             import json
#             with open("results.json", "w") as f:
#                 json.dump(data, f, indent=2)
#
# Exercise 5: Add API key support for OpenWeatherMap
#             Sign up at: https://openweathermap.org/api
#             Use environment variables:
#             import os
#             api_key = os.environ.get("OPENWEATHER_API_KEY")
