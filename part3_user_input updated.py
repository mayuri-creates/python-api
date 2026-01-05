"""
Part 3: Dynamic Queries with User Input
=======================================
Difficulty: Intermediate

Learn:
- Using input() to make dynamic API requests
- Building URLs with f-strings
- Query parameters in URLs
"""


import requests

#  USER INFO 
def get_user_info():
    print("\n=== User Information ===\n")
    user_id = input("Enter user ID (1-10): ").strip()
    if not user_id.isdigit():
        print("Please enter a valid number.")
        return

    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("\nUser Details")
        print("Name:", data["name"])
        print("Email:", data["email"])
        print("Phone:", data["phone"])
    else:
        print("User not found.")

#  POSTS + COMMENTS 
def search_posts_with_comments():
    print("\n=== User Posts & Comments ===\n")
    user_id = input("Enter user ID (1-10): ").strip()
    if not user_id.isdigit():
        print("Please enter a valid number.")
        return

    # Fetch posts
    posts = requests.get("https://jsonplaceholder.typicode.com/posts").json()
    # Fetch comments
    comments = requests.get("https://jsonplaceholder.typicode.com/comments").json()

    found_posts = False
    for post in posts:
        if str(post["userId"]) == user_id:
            found_posts = True
            print(f"\nPost: {post['title']}")
            print("Comments:")
            for comment in comments:
                if comment["postId"] == post["id"]:
                    print("-", comment["name"])
    if not found_posts:
        print("No posts found for this user.")

#  CRYPTO PRICE 
CRYPTO_IDS = {
    "bitcoin": "btc-bitcoin",
    "ethereum": "eth-ethereum",
    "dogecoin": "doge-dogecoin",
    "cardano": "ada-cardano",
    "solana": "sol-solana",
    "ripple": "xrp-xrp"
}

def get_crypto_price():
    print("\n=== Crypto Price ===\n")
    coin_id = input("Enter coin (e.g., btc-bitcoin / eth-ethereum): ").strip().lower()
    coin_id = CRYPTO_IDS.get(coin_id, coin_id)

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        usd = data["quotes"]["USD"]
        print(f"Coin: {data['name']} ({data['symbol']})")
        print(f"Price (USD): ${usd['price']:.2f}")
        print(f"24h Change: {usd['percent_change_24h']:+.2f}%")
    else:
        print("Coin not found.")

#  WEATHER 
CITIES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867)
}

def get_weather():
    print("\n=== Weather Info ===\n")
    print("Available cities:", ", ".join(CITIES.keys()))
    city = input("Enter city: ").lower().strip()
    if city not in CITIES:
        print("City not available.")
        return

    lat, lon = CITIES[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["current_weather"]
        print(f"\nWeather in {city.title()}:")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Wind Speed: {weather['windspeed']} km/h")
    else:
        print("Could not fetch weather.")

# TODOS 
def search_todos():
    print("\n=== Todo Search ===\n")
    status = input("Enter status (true / false): ").lower()
    if status not in ["true", "false"]:
        print("Invalid input.")
        return

    todos = requests.get("https://jsonplaceholder.typicode.com/todos").json()
    filtered = [todo for todo in todos if str(todo["completed"]).lower() == status]
    print(f"Total todos with completed={status}: {len(filtered)}")
    for todo in filtered[:5]:  # Show first 5 for brevity
        print("-", todo["title"])

# DASHBOARD MENU 
def main():
    while True:
        print("\n=== MENU ===")
        print("1. User Info")
        print("2. User Posts + Comments")
        print("3. Crypto Price")
        print("4. Weather Info")
        print("5. Todos by Status")
        print("6. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            get_user_info()
        elif choice == "2":
            search_posts_with_comments()
        elif choice == "3":
            get_crypto_price()
        elif choice == "4":
            get_weather()
        elif choice == "5":
            search_todos()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()




# --- EXERCISES ---
#
# Exercise 1: Add a function to fetch weather for a city
#             Use Open-Meteo API (no key required):
#             https://api.open-meteo.com/v1/forecast?latitude=28.61&longitude=77.23&current_weather=true
#             Challenge: Let user input city name (you'll need to find lat/long)
#
# Exercise 2: Add a function to search todos by completion status
#             URL: https://jsonplaceholder.typicode.com/todos
#             Params: completed=true or completed=false
#
# Exercise 3: Add input validation (check if user_id is a number)
