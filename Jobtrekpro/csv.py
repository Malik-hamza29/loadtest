import csv
import random
from datetime import datetime, timedelta

# Function to generate a random date of birth


def random_dob(start_year=1960, end_year=2000):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    dob = start + timedelta(days=random_days)
    return dob.strftime("%Y-%m-%d")

# Function to generate random phone number


def random_phone():
    return f"+1 ({random.randint(200, 999)}) {random.randint(1000000, 9999999)}"


# Define some options for dynamic fields
specializations = ["Home Cleaning", "Plumbing",
                   "Electrical", "others", "Garage", "handyman"]
skill_levels = ["beginner", "intermediate", "advanced", "expert"]
tags = [{"name": "urgent", "color": "#0055ff"}]

# CSV output file
with open('contractors.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Header
    writer.writerow([
        "firstName", "lastName", "email", "phone", "dateOfBirth",
        "specializations", "skillLevel", "yearsExperience",
        "hourlyRate", "homeBaseAddress",
        "tags", "status"
    ])

    for i in range(1, 601):
        first_name = f"Contractor{i}"
        last_name = f"Test{i}"
        email = f"contractor{i}@yopmail.com"  # Unique email
        phone = random_phone()
        dob = random_dob()
        specialization = random.sample(specializations, 1)
        skill_level = random.choice(skill_levels)
        years_exp = random.randint(1, 50)
        hourly_rate = random.randint(10, 50)
        address = f"Test Address {i}"
        service_radius = random.randint(5, 50)
        service_areas = []  # Keep empty as in your example
        has_vehicle = True
        vehicle_type = random.choice(["truck", "car", "van"])
        owns_tools = True
        license_number = None
        license_state = None
        insurance_provider = None
        emergency_contact_name = None
        emergency_contact_phone = None
        tag_field = str(tags)  # Postman can parse as JSON
        status = "pending"

        writer.writerow([
            first_name, last_name, email, phone, dob,
            str(specialization), skill_level, years_exp,
            hourly_rate, address, service_radius,
            str(service_areas), has_vehicle, vehicle_type,
            owns_tools, license_number, license_state,
            insurance_provider, emergency_contact_name,
            emergency_contact_phone, tag_field, status
        ])

print("CSV with 500 contractors generated successfully!")
