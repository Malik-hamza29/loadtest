import requests
import random
import time

# === CONFIGURATION ===
# Your API endpoint and admin token
API_URL = "https://api.jobtrekpro.com/api/va"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMmMyZjA2Ny03OGJhLTQ1NmQtODU2Yy1mMmMzNzc4YmNjNWUiLCJlbWFpbCI6InRlc3RAeW9wbWFpbC5jb20iLCJyb2xlIjoib3duZXIiLCJpYXQiOjE3NjMwMjkwMDQsImV4cCI6MTc2MzExNTQwNH0.ohdkrHCQS8WDSFYCkrIW7vlCFdVwZ4lttUXgf61jM8A"  # Replace with your real admin token
BASE_EMAIL = "va@yopmail.com"  # Yopmail for temporary clients

# Request headers
headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

# Random name generation
first_names = ["Chelsea", "Alex", "Jordan",
               "Taylor", "Morgan", "Casey", "Riley", "Jamie"]
last_names = ["Barber", "Smith", "Johnson", "Lee", "Brown", "Clark", "Adams"]


def generate_client(i):
    """Generates a client payload with random data"""
    first = random.choice(first_names)
    last = random.choice(last_names)

    # Generate a unique email using a Yopmail alias
    base_name = BASE_EMAIL.split("@")[0]
    domain = BASE_EMAIL.split("@")[1]
    email = f"{base_name}+{i}@{domain}"

    # Create the client payload with random data
    payload = {
        "first_name": first,
        "last_name": last,
        "email": email,
        # Random phone number
        "mobile_number": f"+1 (800) {random.randint(1000000, 9999999)}",
        # "address": "1234 Placeholder St",  # Placeholder address
        # "notes": "Sample client information",  # Placeholder notes

    }

    return payload


def create_clients(n=500):
    """Creates n clients and sends the data to the API"""
    success, fail = 0, 0
    for i in range(1, n + 1):
        payload = generate_client(i)
        try:
            # Send the POST request to create a client
            response = requests.post(
                API_URL, json=payload, headers=headers, timeout=10)

            if response.status_code in [200, 201]:
                success += 1
                print(f"[{i}] ✅ Created VA: {payload['email']}")
            else:
                fail += 1
                print(f"[{i}] ❌ Failed ({response.status_code}): {response.text}")
        except Exception as e:
            fail += 1
            print(f"[{i}] ⚠️ Exception: {e}")

        # Optional: Add a small delay to avoid hitting rate limits
        time.sleep(0.1)

    print(f"\n✅ Success: {success} | ❌ Failed: {fail}")


if __name__ == "__main__":
    create_clients(400)  # Create 500 clients for testing
