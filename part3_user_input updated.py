"""
Part 3: Dynamic Queries with User Input
=======================================
Difficulty: Intermediate

Learn:
- Using input() to make dynamic API requests
- Building URLs with f-strings
- Query parameters in URLs
"""

"""
Part 3: Dynamic Queries with User Input
=======================================
Difficulty: Intermediate
"""

import requests


def get_user_info():
    print("\nUser Information\n")

    user_id = input("Enter user ID (1-10): ")

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


def search_posts():
    print("\nPost Search\n")

    user_id = input("Enter user ID (1-10): ")

    if not user_id.isdigit():
        print("Please enter a valid number.")
        return

    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": user_id}

    response = requests.get(url)
    posts = response.json()

    print("\nPosts:")
    for post in posts:
        if str(post["userId"]) == user_id:
            print("-", post["title"])


def get_crypto_price():
    print("\nCrypto Price\n")

    coin_id = input("Enter coin ID (btc-bitcoin / eth-ethereum): ").strip().lower()

    url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price = data["quotes"]["USD"]["price"]
        print("Coin:", data["name"])
        print("Price (USD):", round(price, 2))
    else:
        print("Coin not found.")



# Exercise 1: Weather Function


def get_weather():
    print("\nWeather Info\n")

    print("Cities available: Delhi, Mumbai")
    city = input("Enter city name: ").lower()

    if city == "delhi":
        lat, lon = 28.61, 77.23
    elif city == "mumbai":
        lat, lon = 19.07, 72.87
    else:
        print("City not available.")
        return

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)

    data = response.json()
    weather = data["current_weather"]

    print("Temperature:", weather["temperature"], "°C")
    print("Wind Speed:", weather["windspeed"], "km/h")


# Exercise 2: Search Todos by Status


def search_todos():
    print("\nTodo Search\n")

    status = input("Enter status (true / false): ").lower()

    if status not in ["true", "false"]:
        print("Invalid input.")
        return

    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url)
    todos = response.json()

    count = 0
    for todo in todos:
        if str(todo["completed"]).lower() == status:
            count += 1

    print("Total todos with completed =", status, ":", count)


def main():
    while True:
        print("\nMenu")
        print("1. User info")
        print("2. User posts")
        print("3. Crypto price")
        print("4. Weather")
        print("5. Todos")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            get_user_info()
        elif choice == "2":
            search_posts()
        elif choice == "3":
            get_crypto_price()
        elif choice == "4":
            get_weather()
        elif choice == "5":
            search_todos()
        elif choice == "6":
            print("Program ended.")
            break
        else:
            print("Wrong choice.")


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
