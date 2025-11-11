import requests
import random
import time

# === CONFIGURATION ===
# ← replace with your API endpoint for clients
API_URL = "https://api.jobtrekpro.com/api/clients"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJkY2YwZGUxNS1lNDk4LTRjMzQtOGQ5OC04N2UwOTIwNTcyNTEiLCJlbWFpbCI6IjEybm92QHlvcG1haWwuY29tIiwicm9sZSI6Im93bmVyIiwiaWF0IjoxNzYyODgxMzEyLCJleHAiOjE3NjI5Njc3MTJ9.Er2gF1swESD5TeTNBegyEp-C7QdU6EGz2DMlIsQQp54"  # ← replace with your real admin token
BASE_EMAIL = "user@yopmail.com"  # Yopmail for temporary clients

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

# Random names, email generation
first_names = ["Chelsea", "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie"]
last_names = ["Barber", "Smith", "Johnson", "Lee", "Brown", "Clark", "Adams"]

def generate_client(i):
    first = random.choice(first_names)
    last = random.choice(last_names)

    # YOPmail unique alias — all deliver to the same inbox
    base_name = BASE_EMAIL.split("@")[0]
    domain = BASE_EMAIL.split("@")[1]
    email = f"{base_name}+{i}@{domain}"

    payload = {
        "name": f"{first} {last}",
        "email": email,
        "phone": f"+1 (800) {random.randint(1000000, 9999999)}",
        "address": "Voluptatem Dignissi",  # Placeholder address
        "notes": "Lorem ipsum dolor sit amet.",  # Placeholder notes
         "tags": ["urgent"],   # Optional tags
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
                print(f"[{i}] ✅ Created client: {payload['email']}")
            else:
                fail += 1
                print(f"[{i}] ❌ Failed ({response.status_code}): {response.text}")
        except Exception as e:
            fail += 1
            print(f"[{i}] ⚠️ Exception: {e}")

        # Optional: prevent backend rate-limiting
        time.sleep(0.1)

    print(f"\n✅ Success: {success} | ❌ Failed: {fail}")


if __name__ == "__main__":
    create_clients(500)  # Create 3 clients for testing
