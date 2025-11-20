import requests
import random
import time
from datetime import datetime, timedelta

# === CONFIGURATION ===
API_URL = "https://api.jobtrekpro.com/api/contractors"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJmZTYwMjIzMy02Njg0LTRmYjYtYWJkOC0xNjk0ZTIyMzgzYzAiLCJlbWFpbCI6Im1hbnVhbHRlc3RpbmdAeW9wbWFpbC5jb20iLCJyb2xlIjoib3duZXIiLCJpYXQiOjE3NjM2MTM4MzYsImV4cCI6MTc2MzcwMDIzNn0.b7WDnGy19WYU_o4s4ln__dvVMPxLT43h1riOmdJ0Snk"
BASE_EMAIL = "cont@yopmail.com"

# Request headers
headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

# Random data pools
first_names = [
    'John', 'Michael', 'David', 'James', 'Robert', 'William',
    'Sarah', 'Jennifer', 'Lisa', 'Mary', 'Patricia', 'Linda',
    'Ahmed', 'Ali', 'Hassan', 'Fatima', 'Aisha', 'Zainab',
    'Chris', 'Daniel', 'Matthew', 'Emma', 'Olivia', 'Sophia',
    'Illana', 'Carlos', 'Marcus', 'Elena', 'Diego', 'Isabella'
]

last_names = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
    'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez',
    'Khan', 'Ahmed', 'Ali', 'Hassan', 'Malik', 'Shah',
    'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson',
    'Dickson', 'Cooper', 'Bennett', 'Foster', 'Coleman'
]

# Tag options
TAG_NAMES = [
    "urgent", "vip", "priority", "certified", "active",
    "verified", "expert", "reliable", "preferred", "new-hire"
]

TAG_COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B195', '#C06C84',
    '#6C5B7B', '#355C7D', '#F67280', '#C8E6C9', '#FFCCBC',
    '#0055ff', '#ff5500', '#00ff55', '#5500ff', '#ff0055'
]

# Specializations
SPECIALIZATIONS = [
    "electrical", "plumbing", "hvac", "carpentry", "painting",
    "roofing", "cleaning", "landscaping"
]

# Skill levels - THIS WILL BE RANDOMLY SELECTED EACH TIME
SKILL_LEVELS = ["beginner", "intermediate", "advanced", "expert"]

# Vehicle types
# Removed None - will handle separately
VEHICLE_TYPES = ["car", "truck", "van", "suv"]

# Home base addresses
ADDRESSES = [
    "123 Main Street",
    "456 Oak Avenue",
    "789 Elm Boulevard",
    "321 Pine Road",
    "654 Maple Drive",
    "987 Cedar Lane",
    "147 Birch Street",
    "258 Willow Way",
    "369 Aspen Court",
    "741 Spruce Avenue"
]


def generate_random_dob():
    """Generate random date of birth (age between 21-65)"""
    today = datetime.now()
    years_ago = random.randint(21, 65)
    dob = today - timedelta(days=years_ago * 365 + random.randint(0, 364))
    return dob.strftime("%Y-%m-%d")


def generate_contractor(i):
    """Generates a contractor payload with random data"""
    first = random.choice(first_names)
    last = random.choice(last_names)

    # Generate unique email using Yopmail alias
    base_name = BASE_EMAIL.split("@")[0]
    domain = BASE_EMAIL.split("@")[1]
    email = f"{base_name}+{i}@{domain}"

    # SELECT ONLY ONE TAG (randomly each time)
    selected_tag_name = random.choice(TAG_NAMES)
    tags = [{"name": selected_tag_name, "color": random.choice(TAG_COLORS)}]

    # SELECT ONLY ONE SPECIALIZATION (randomly each time)
    specializations = [random.choice(SPECIALIZATIONS)]

    # RANDOMLY SELECT SKILL LEVEL (this happens fresh for each contractor)
    skill_level = random.choice(SKILL_LEVELS)

    # Random boolean values
    has_vehicle = random.choice([True, False])
    owns_tools = random.choice([True, False])

    # If has vehicle, always select a vehicle type (not None)
    vehicle_type = random.choice(VEHICLE_TYPES) if has_vehicle else None

    # Create the contractor payload
    payload = {
        "firstName": first,
        "lastName": last,
        "email": email,
        "phone": f"+1 ({random.randint(100, 999)}) {random.randint(1000000, 9999999)}",
        "dateOfBirth": generate_random_dob(),
        "homeBaseAddress": random.choice(ADDRESSES),
        "serviceRadius": random.choice([10, 15, 25, 30, 50]),
        "hourlyRate": random.randint(20, 100),
        "yearsExperience": random.randint(1, 40),
        "skillLevel": skill_level,  # Using the randomly selected skill level
        "specializations": specializations,
        "hasVehicle": has_vehicle,
        # Will be a valid type if hasVehicle=True, None otherwise
        "vehicleType": vehicle_type,
        "ownsTools": owns_tools,
        "tags": tags,
        "serviceAreas": [],
        "licenseNumber": None,
        "licenseState": None,
        "insuranceProvider": None,
        "emergencyContactName": None,
        "emergencyContactPhone": None
    }

    return payload


def create_contractors(n=10):
    """Creates n contractors and sends the data to the API"""
    success, fail = 0, 0

    print(f"\n🚀 Creating {n} contractors...")
    print("=" * 80)

    for i in range(1, n + 1):
        payload = generate_contractor(i)
        try:
            # Send the POST request to create a contractor
            response = requests.post(
                API_URL, json=payload, headers=headers, timeout=10)

            if response.status_code in [200, 201]:
                success += 1
                tag_name = payload['tags'][0]['name']
                spec_name = payload['specializations'][0]
                print(
                    f"[{i}] ✅ {payload['firstName']} {payload['lastName']} | {payload['email']}")
                print(
                    f"     📋 {payload['skillLevel']} | {payload['yearsExperience']}yrs | ${payload['hourlyRate']}/hr")
                print(f"     🏷️  Tag: {tag_name} | Spec: {spec_name}")
            else:
                fail += 1
                print(f"[{i}] ❌ Failed ({response.status_code}): {response.text}")
        except Exception as e:
            fail += 1
            print(f"[{i}] ⚠️ Exception: {e}")

        # Small delay to avoid rate limits
        time.sleep(0.1)

    print("=" * 80)
    print(f"\n✨ Completed! ✅ Success: {success} | ❌ Failed: {fail}")
    print(
        f"📬 All emails accessible at: https://yopmail.com/{BASE_EMAIL.split('@')[0]}")


if __name__ == "__main__":
    # Create 20 contractors for testing
    create_contractors(10)

    # For larger batches:
    # create_contractors(50)
    # create_contractors(100)
