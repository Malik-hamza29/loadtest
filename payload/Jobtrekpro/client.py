import requests
import random
import time
# === CONFIGURATION ===
# ← replace with your API endpoint for clients
API_URL = "https://api.jobtrekpro.com/api/clients"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJkMzZhN2UyZi01OTg1LTQ5YTYtYTg0Ny01YzdhMjQ3MTk3MzkiLCJlbWFpbCI6IjE3bm92QHlvcG1haWwuY29tIiwicm9sZSI6Im93bmVyIiwiaWF0IjoxNzYzMzU5ODE5LCJleHAiOjE3NjM0NDYyMTl9.PouXhCU6pqkcSHzlgplrkyONGO68-LVoIXQxwchxIns"  # ← replace with your real admin token
BASE_EMAIL = "client1@yopmail.com"  # Yopmail for temporary clients
headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}
# Random names, email generation
first_names = ["Chelsea", "Alex", "Jordan",
               "Taylor", "Morgan", "Casey", "Riley", "Jamie"]
last_names = ["Barber", "Smith", "Johnson", "Lee", "Brown", "Clark", "Adams"]
# Available tags and colors
tags = ["urgent", "vip", "priority", "new", "active",
        "pending", "follow-up", "hot-lead", "qualified", "prospect"]
tag_colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33F5",
              "#F5FF33", "#33FFF5", "#FF8C33", "#8C33FF", "#33FF8C", "#FF3333"]


def generate_client(i):
    first = random.choice(first_names)
    last = random.choice(last_names)
    # YOPmail unique alias — all deliver to the same inbox
    base_name = BASE_EMAIL.split("@")[0]
    domain = BASE_EMAIL.split("@")[1]
    email = f"{base_name}+{i}@{domain}"
    # Randomly select a tag and color
    selected_tag = random.choice(tags)
    selected_color = random.choice(tag_colors)
    payload = {
        "name": f"{first} {last}",
        "email": email,
        "phone": f"+1 (800) {random.randint(1000000, 9999999)}",
        "address": "Voluptatem Dignissi",  # Placeholder address
        "notes": "Lorem ipsum dolor sit amet.",  # Placeholder notes
        "tags": [selected_tag],  # Randomly selected tag
        "color": selected_color,  # Randomly selected color
    }
    return payload


def create_clients(n=500):
    success, fail = 0, 0
    for i in range(1, n + 1):
        payload = generate_client(i)
        try:
            response = requests.post(
                API_URL, json=payload, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                success += 1
                print(f"[{i}]: Created client: {payload['email']}")
            else:
                fail += 1
                print(f"[{i}] :x: Failed ({response.status_code}): {response.text}")
        except Exception as e:
            fail += 1
            print(f"[{i}] :warning: Exception: {e}")
        # Optional: prevent backend rate-limiting
        time.sleep(0.1)
    print(f"\n:created client: Success: {success} | :x: Failed: {fail}")


if __name__ == "__main__":
    create_clients(50)  # Create 500 clients
