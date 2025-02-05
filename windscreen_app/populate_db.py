from windscreen_app.models import VehicleMake, VehicleModel, InsuranceProvider, Windscreen, WindscreenCategory, Category # type: ignore

# Define 15 common vehicle makes
vehicle_makes = [
    "Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW", "Mercedes-Benz", 
    "Volkswagen", "Audi", "Hyundai", "Kia", "Mazda", "Subaru", "Jeep", "Tesla"
]

# Define 6 models for each make
vehicle_models = {
    "Toyota": ["Corolla", "Camry", "Rav4", "Highlander", "Yaris", "Hilux"],
    "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Fit", "Pilot"],
    "Ford": ["F-150", "Mustang", "Escape", "Edge", "Explorer", "Focus"],
    "Chevrolet": ["Silverado", "Equinox", "Malibu", "Tahoe", "Suburban", "Camaro"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder", "Frontier", "Murano"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "M3", "7 Series"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE", "A-Class", "S-Class"],
    "Volkswagen": ["Golf", "Jetta", "Passat", "Tiguan", "Atlas", "ID.4"],
    "Audi": ["A3", "A4", "Q3", "Q5", "Q7", "A6"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Kona", "Palisade"],
    "Kia": ["Rio", "Forte", "Optima", "Sportage", "Sorento", "Telluride"],
    "Mazda": ["Mazda3", "Mazda6", "CX-3", "CX-5", "CX-9", "MX-5"],
    "Subaru": ["Impreza", "Legacy", "Forester", "Outback", "WRX", "Ascent"],
    "Jeep": ["Wrangler", "Grand Cherokee", "Cherokee", "Renegade", "Compass", "Gladiator"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Roadster", "Cybertruck"]
}

# Insert into the database
for make_name in vehicle_makes:
    make, _ = VehicleMake.objects.get_or_create(name=make_name)
    for model_name in vehicle_models[make_name]:
        VehicleModel.objects.get_or_create(make=make, name=model_name)

print("Vehicle Makes and Models added successfully.")
# Define 15 random insurance providers and their windscreen costs
insurance_providers = [
    ("Allianz", 250.00), ("State Farm", 275.00), ("Geico", 230.00), 
    ("Progressive", 260.00), ("Nationwide", 240.00), ("Liberty Mutual", 280.00),
    ("Farmers", 235.00), ("USAA", 290.00), ("Travelers", 245.00), 
    ("MetLife", 270.00), ("American Family", 255.00), ("AXA", 300.00),
    ("The Hartford", 285.00), ("Chubb", 310.00), ("Erie Insurance", 265.00)
]

# Define a category for insurance providers
insurance_category, _ = Category.objects.get_or_create(name="Insurance")

# Insert data into the database
for name, cost in insurance_providers:
    InsuranceProvider.objects.get_or_create(
        name=name, cost=cost, coverage_type="Comprehensive", category=insurance_category
    )

print("Insurance Providers added successfully.")
# Define windscreen categories
windscreen_categories = [
    "Standard", "Luxury", "Performance", "SUV", "Electric"
]

# Insert windscreen categories
for category_name in windscreen_categories:
    WindscreenCategory.objects.get_or_create(name=category_name, description=f"{category_name} windscreen category")

# Define windscreen types
windscreen_types = [
    "Heated", "Non-Heated", "Plain with Camera", "Without Camera",
    "With Two Cameras", "Without Cameras", "Fully Heated", "Partially Heated"
]

# Insert windscreen types
for windscreen_type in windscreen_types:
    category = WindscreenCategory.objects.order_by('?').first()  # Random category assignment
    Windscreen.objects.get_or_create(
        type=windscreen_type, category=category, make="Generic", model="Universal"
    )

print("Windscreen Types added successfully.")

