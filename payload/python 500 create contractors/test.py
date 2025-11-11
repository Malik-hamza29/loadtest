import requests
import random
import time

# === CONFIGURATION ===
API_URL = "https://api.jobtrekpro.com/api/contractors"
# Use an environment variable or a config file for security
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJkY2YwZGUxNS1lNDk4LTRjMzQtOGQ5OC04N2UwOTIwNTcyNTEiLCJlbWFpbCI6IjEybm92QHlvcG1haWwuY29tIiwicm9sZSI6Im93bmVyIiwiaWF0IjoxNzYyODgxMzEyLCJleHAiOjE3NjI5Njc3MTJ9.Er2gF1swESD5TeTNBegyEp-C7QdU6EGz2DMlIsQQp54"
BASE_EMAIL = "test@yopmail.com"

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

first_names = ["john", "Alex", "Jordan",
               "Taylor", "Morgan", "ciri", "Riley", "Jamie"]
last_names = ["Barber", "carlson", "Johnson",
              "Lee", "charles", "Clark", "Adams"]

# List of specializations
specializations = ["electrical", "handyman", "garage", "plumbing", "others"]


def generate_contractor(i):
    first = random.choice(first_names)
    last = random.choice(last_names)

    # YOPmail unique alias — all deliver to the same inbox
    base_name = BASE_EMAIL.split("@")[0]
    domain = BASE_EMAIL.split("@")[1]
    email = f"{base_name}+{i}@{domain}"

    # Select a random specialization
    specialization = random.choice(specializations)

    # Payload for contractor creation
    payload = {
        "firstName": first,
        "lastName": last,
        "email": email,
        "dateOfBirth": "1995-06-30",
        "phone": f"+1 (800) {random.randint(1000000, 9999999)}",
        "homeBaseAddress": "Voluptatem Dignissi",
        "hourlyRate": 55,
        "serviceRadius": 25,
        "skillLevel": "beginner",
        # Using the random specialization
        "specialization": [specialization],
        "status": "pending",
        "tags": [{"name": "maintenance", "color": "#0055ff"}],
        "hasVehicle": False,
        "ownsTools": False,
        "yearsExperience": 20,
        "serviceAreas": [],
        "emergencyContactName": None,
        "emergencyContactPhone": None,
        "insuranceProvider": None,
        "licenseNumber": None,
        "licenseState": None,
        "vehicleType": None
    }

    return payload


def create_contractors(n=500):
    success, fail = 0, 0
    for i in range(1, n + 1):
        payload = generate_contractor(i)
        try:
            # Send the POST request to create a contractor
            response = requests.post(
                API_URL, json=payload, headers=headers, timeout=10)

            if response.status_code in [200, 201]:
                success += 1
                print(f"[{i}] ✅ Created contractor: {payload['email']}")
            else:
                fail += 1
                print(f"[{i}] ❌ Failed ({response.status_code}): {response.text}")

        except requests.exceptions.RequestException as e:
            # Catch network-related errors
            fail += 1
            print(f"[{i}] ⚠️ Exception: {e}")

        # Optional: prevent backend rate-limiting
        time.sleep(0.1)

    print(f"\n✅ Success: {success} | ❌ Failed: {fail}")


if __name__ == "__main__":
    create_contractors(3)
