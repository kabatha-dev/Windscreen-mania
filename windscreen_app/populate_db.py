import random
from django.db import transaction
from windscreen_app.models import Vehicle, Service, Quote, Order, InsuranceProvider, WindscreenType, WindscreenCustomization, ServiceCost

def generate_vehicle_data():
    # 10 common vehicle makes in Kenya
    makes = ["Toyota", "Honda", "Nissan", "Mitsubishi", "Mazda", "Kia", "Hyundai", "BMW", "Ford", "Suzuki"]
    vehicle_models = {
        "Toyota": ["Corolla", "Fortuner", "Prado", "Land Cruiser", "Hilux", "Camry", "Vitz", "RAV4", "Avensis", "Land Cruiser 70", "Yaris", "Allion", "Mark X", "Axio", "Sienta"],
        "Honda": ["Civic", "Accord", "CR-V", "Fit", "Pilot", "Odyssey", "Insight", "HR-V", "Jazz", "Stream", "Element", "Ridgeline", "CR-Z", "Clarity", "Elysion"],
        "Nissan": ["Navara", "X-Trail", "Almera", "Juke", "Murano", "Maxima", "Patrol", "Altima", "Sentra", "Leaf", "Pathfinder", "Frontier", "Armada", "Versa", "370Z"],
        "Mitsubishi": ["Outlander", "Pajero", "Lancer", "ASX", "Eclipse", "Mirage", "Delica", "RVR", "Montero", "Galant", "Shogun", "Fuso", "Mighty", "FTO", "3000GT"],
        "Mazda": ["CX-5", "Mazda 3", "Mazda 6", "CX-9", "Mazda 2", "MX-5", "CX-30", "Mazda 323", "Mazda 5", "Mazda 6 Sport", "Mazda 2 Sport", "Mazda 2 Classic", "Mazda CX-7", "Mazda 121", "Mazda RX-8"],
        "Kia": ["Sportage", "Seltos", "Picanto", "Sorento", "Ceed", "Stinger", "K900", "K9", "Niro", "Forte", "Optima", "Soul", "Cadenza", "Carnival", "Ray"],
        "Hyundai": ["Elantra", "Sonata", "Tucson", "Kona", "Palisade", "Santa Fe", "Veloster", "Creta", "Ioniq", "i20", "i30", "Nexo", "Genesis", "Azera", "Coupe"],
        "BMW": ["X5", "X3", "3 Series", "5 Series", "7 Series", "X1", "Z4", "M3", "M4", "X6", "2 Series", "i3", "i8", "i4", "iX"],
        "Ford": ["Focus", "Ranger", "Fiesta", "F-150", "Escape", "Mustang", "Explorer", "Fusion", "Edge", "Taurus", "Expedition", "Mondeo", "C-Max", "Transit", "Kuga"],
        "Suzuki": ["Vitara", "Swift", "Baleno", "Alto", "Celerio", "Jimny", "SX4", "Grand Vitara", "Liana", "Wagon R", "Ertiga", "Kizashi", "Swift Sport", "Celerio Hybrid", "Ignis"]
    }

    # Insert 10 makes and 15 models for each
    vehicles = []
    for make, models in vehicle_models.items():
        for model in models:
            vehicle = Vehicle.objects.create(
                registration_number=f"REG{random.randint(1000, 9999)}",
                year_of_make=random.randint(2000, 2023),
            )
            vehicles.append(vehicle)

    return vehicles

def generate_service_data():
    # Service types
    services = [
        "Tyre Change and Repair",
        "Windscreen Replacement",
        "Tints",
        "Body Works",
        "Alignment"
    ]
    service_objects = []
    for service_name in services:
        service = Service.objects.create(
            name=service_name,
            cost=random.uniform(1000, 5000)
        )
        service_objects.append(service)
    return service_objects

def generate_insurance_data():
    insurance_companies = [
        "Jubilee Insurance", "Kenya Re", "Britam", "APA Insurance", "UAP Old Mutual",
        "CIC Insurance", "The Jubilee Insurance Company", "Kenindia Assurance", "Sanlam Kenya", "AIG Kenya",
        "Madison Insurance", "First Assurance", "Invesco Assurance", "Heritage Insurance", "Amaco Insurance",
        "GA Insurance", "Minet Kenya", "Allianz Insurance", "Old Mutual", "Fidelity Shield"
    ]
    insurance_objects = []
    for company_name in insurance_companies:
        insurance = InsuranceProvider.objects.create(name=company_name)
        insurance_objects.append(insurance)
    return insurance_objects

def generate_windscreen_data():
    windscreen_types = [
        "Windshield", "Quarter Glass", "Rear Right", "Rear Left"
    ]
    windscreen_customizations = {
        "Windshield": 10,
        "Quarter Glass": 5,
        "Rear Right": 5,
        "Rear Left": 5
    }
    
    windscreen_objects = []
    customization_objects = []
    
    for windscreen_type in windscreen_types:
        windscreen = WindscreenType.objects.create(name=windscreen_type)
        windscreen_objects.append(windscreen)
        
        for _ in range(windscreen_customizations.get(windscreen_type, 0)):
            customization = WindscreenCustomization.objects.create(
                windscreen_type=windscreen,
                customization_details=f"Customization {random.randint(1, 100)}"
            )
            customization_objects.append(customization)
    return windscreen_objects, customization_objects

def generate_service_costs(vehicles, services):
    for vehicle in vehicles:
        for service in services:
            cost = random.uniform(1000, 5000)  # Random cost simulation based on service
            ServiceCost.objects.create(
                vehicle=vehicle,
                service=service,
                cost=cost
            )

# Main function to populate the database
def populate_database():
    with transaction.atomic():
        vehicles = generate_vehicle_data()
        services = generate_service_data()
        insurance_companies = generate_insurance_data()
        windscreen_types, customizations = generate_windscreen_data()
        generate_service_costs(vehicles, services)

        print("Database populated successfully.")

if __name__ == "__main__":
    populate_database()
