import requests
import random
import time

# === CONFIGURATION ===
# ← replace with your API endpoint
API_URL = "https://api.jobtrekpro.com/api/contractors"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMmMyZjA2Ny03OGJhLTQ1NmQtODU2Yy1mMmMzNzc4YmNjNWUiLCJlbWFpbCI6InRlc3RAeW9wbWFpbC5jb20iLCJyb2xlIjoib3duZXIiLCJpYXQiOjE3NjMwMjgzOTUsImV4cCI6MTc2MzExNDc5NX0.d2XV4_cav7dJY3qVK2pV5G9xbmHGZJOxgRbiJMkqZg4"              # ← replace with your real admin token
# ← base inbox (check on yopmail.com/?testuser)
BASE_EMAIL = "con@yopmail.com"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMmMyZjA2Ny03OGJhLTQ1NmQtODU2Yy1mMmMzNzc4YmNjNWUiLCJlbWFpbCI6InRlc3RAeW9wbWFpbC5jb20iLCJyb2xlIjoib3duZXIiLCJpYXQiOjE3NjMwMjgzOTUsImV4cCI6MTc2MzExNDc5NX0.d2XV4_cav7dJY3qVK2pV5G9xbmHGZJOxgRbiJMkqZg4",
    "Content-Type": "application/json"
}


first_names = ["Chelsea", "Alex", "Jordan",
               "Taylor", "Morgan", "Casey", "Riley", "Jamie"]
last_names = ["Barber", "Smith", "Johnson", "Lee", "Brown", "Clark", "Adams"]


# 🧰 Add your possible specializations here
specializations_list = ["garage", "plumbing", "electrical", "hvac",
                        "landscaping", "carpentry", "painting", "roofing", "cleaning"]
tags_list = ["urgent", "vip", "new", "experienced",
             "part time", "full time", "ontime"]
colors_list = ["#0055ff", "#ff0000", "#00cc00",
               "#ffaa00", "#cc00ff", "#00cccc", "#ff6600", "#0099ff"]


def generate_contractor(i):
    first = random.choice(first_names)
    last = random.choice(last_names)
    # Select only 1 random specialization
    specialization = random.choice(specializations_list)
    specializations = [specialization]
    tag = random.choice(tags_list)
    tag_color = random.choice(colors_list)

    # YOPmail unique alias — all deliver to same inbox
    base_name = BASE_EMAIL.split("@")[0]
    domain = BASE_EMAIL.split("@")[1]
    email = f"{base_name}+{i}@{domain}"

    payload = {
        "firstName": first,
        "lastName": last,
        "email": email,
        "dateOfBirth": "1995-06-30",
        "phone": f"+1 (800) {random.randint(1000000, 9999999)}",
        "homeBaseAddress": "Voluptatem Dignissi",
        "hourlyRate": 10,
        "serviceRadius": 25,
        "skillLevel": "beginner",
        # 🎯 Random specializations
        "specializations": specializations,
        "status": "pending",
        "tags": [{"name": tag, "color": tag_color}],
        "hasVehicle": False,
        "ownsTools": False,
        "yearsExperience": 10,
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
            response = requests.post(
                API_URL, json=payload, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                success += 1
                print(f"[{i}] ✅ Created contractor: {payload['email']}")
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
    create_contractors(5)
