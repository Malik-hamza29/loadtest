import csv
import random

# Define categories
categories = [
    "Air Duct Cleaning", "Electrical", "Plumbing", "Automotive", "Carpet Cleaning",
    "Appliances", "Garage", "General Contractor", "Handyman", "Heating and Air Conditioning",
    "Landscaping and Lawn", "Pest Control", "Window and Exterior Cleaning", "Other"
]

# Function to generate random numeric values


def random_price(min_val, max_val):
    return round(random.uniform(min_val, max_val), 2)

# Function to generate a sample description


def sample_description(category):
    return f"Sample service description for {category.lower()}."


# Create CSV file
with open("services.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow([
        "Category Name", "Category Image", "Name", "Image", "Description",
        "Duration", "Base Price", "Materials Cost", "Markup Percent", "Keywords"
    ])

    # Generate sample data
    for category in categories:
        category_image = f"{category.lower().replace(' ', '_')}.jpg"
        service_name = f"Sample {category} Service"
        service_image = f"{category.lower().replace(' ', '_')}_service.jpg"
        description = sample_description(category)
        duration = f"{random.randint(1, 5)} hours"
        base_price = random_price(50, 500)
        materials_cost = random_price(10, 200)
        markup_percent = random.randint(10, 40)
        keywords = f"{category.lower().replace(' ', ', ')}, service"

        # Write row
        writer.writerow([
            category, category_image, service_name, service_image, description,
            duration, base_price, materials_cost, markup_percent, keywords
        ])

print("CSV file 'services.csv' created successfully!")
