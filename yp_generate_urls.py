''' Generate URLs for subsequent download from YP
'''

output_file = "yp_urls.txt"

states_all = False
states = [
	# "ak",
	# "al",
	# "ar",
	# "az",
	# "ca",
	# "co",
	# "ct",
	# "dc",
	# "de",
	# "fl",
	# "ga",
	# "hi",
	# "ia",
	# "id",
	# "il",
	# "in",
	# "ks",
	# "ky",
	# "la",
	# "ma",
	# "md",
	# "me",
	# "mi",
	# "mn",
	# "mo",
	# "ms",
	# "mt",
	# "nc",
	# "nd",
	# "ne",
	# "nh",
	# "nj",
	# "nm",
	# "nv",
	# "ny",
	# "oh",
	# "ok",
	# "or",
	# "pa",
	# "ri",
	# "sc",
	# "sd",
	# "tn",
	# "tx",
	# "ut",
	# "va",
	# "vt",
	# "wa",
	# "wi",
	# "wv",
	# "wy",
]

categories = [
	# HOME SERVICES

	# "storage-units",
	 "plumbers",
	# "electricians",
	# "carpet-rug-cleaners",
	# "movers",
	# "pest-control-services",
	# "self-storage",
	# "major-appliance-refinishing-repair",
	# "garage-doors-openers",
	# "major-appliance-parts",
	# "house-cleaning",
	# "lawn-mowers-sharpening-repairing",
	# "moving-equipment-rental",
	# "air-conditioning-service-repair",
	# "security-control-systems-monitoring",
	# "garden-centers",
	# "refrigerators-freezers-repair-service",
	# "nurseries-plants-trees",
	# "tree-service",
	# "general-contractors",

	# MEDICAL SERVICES

	# "dentists",
	# "physicians-surgeons-dermatology",
	# "optometrists",
	# "physical-therapists",
	# "hospitals",
	# "physicians-surgeons-endocrinology-diabetes-metabolism",
	# "physicians-surgeons-gynecology",
	# "physicians-surgeons-podiatrists",
	# "physicians-surgeons-neurology",
	# "physicians-surgeons-ophthalmology",
	# "physicians-surgeons-gastroenterology-stomach-intestines",
	# "physicians-surgeons-pediatrics",
	# "orthodontists",
	# "physicians-surgeons-urology",
	# "physicians-surgeons-rheumatology-arthritis",
	# "physicians-surgeons-obstetrics-and-gynecology",
	# "physicians-surgeons",
	# "physicians-surgeons-cardiology",
	# "physicians-surgeons-radiology",
	# "pediatric-dentistry",

	# AUTO SERVICES

	# "automobile-parts-supplies",
	# "auto-oil-lube",
	# "tire-dealers",
	# "auto-repair-service",
	# "window-tinting",
	# "towing",
	# "automobile-body-repairing-painting",
	# "automobile-detailing",
	# "automotive-roadside-service",
	# "windshield-repair",
	# "tire-recap-retread-repair",
	# "automobile-salvage",
	# "glass-auto-plate-window-etc",
	# "automobile-accessories",
	# "wheels-aligning-balancing",
	# "used-rebuilt-auto-parts",
	# "automobile-transporters",
	# "dent-removal",
	# "radiators-automotive-sales-service",
	# "automobile-alarms-security-systems",

	# LEGAL SERVICES

	# "attorneys",
	# "bail-bonds",
	# "private-investigators-detectives",
	# "stenographers-public",
	# "divorce-attorneys",
	# "lie-detection-service",
	# "automobile-accident-attorneys",
	# "family-law-attorneys",
	# "bankruptcy-law-attorneys",
	# "process-servers",
	# "tax-attorneys",
	# "fingerprinting",
	# "medical-malpractice-attorneys",
	# "accident-property-damage-attorneys",
	# "child-custody-attorneys",
	# "business-law-attorneys",
	# "immigration-law-attorneys",
	# "employee-benefits-worker-compensation-attorneys",
	# "dui-dwi-attorneys",
	# "civil-litigation-trial-law-attorneys",
	# "labor-employment-law-attorneys",

	# RESTAURANTS

	# "mexican-restaurants",
	# "sushi-bars",
	# "chinese-restaurants",
	# "italian-restaurants",
	# "thai-restaurants",
	# "breakfast-brunch-lunch-restaurants",
	# "seafood-restaurants",
	# "vegetarian-restaurants",
	# "korean-restaurants",
	# "cuban-restaurants",
	# "greek-restaurants",
	# "soul-food-restaurants",
	# "japanese-restaurants",
	# "french-restaurants",
	# "german-restaurants",
	# "brazilian-restaurants",

	# INSURANCE

	# "auto-insurance",
	# "boat-marine-insurance",
	# "business-commercial-insurance",
	# "dental-insurance",
	# "workers-compensation-disability-insurance",
	# "flood-insurance",
	# "homeowners-insurance",
	# "insurance",
	# "liability-malpractice-insurance",
	# "life-insurance",
	# "long-term-care-insurance",
	# "motorcycle-insurance",
	# "pet-insurance",
	# "renters-insurance",
	# "recreational-vehicle-insurance",
	# "title-mortgage-insurance",
	# "travel-insurance",
	# "truck-insurance",

	# PET SERVICES

	# "animal-shelters",
	# "dog-training",
	# "dog-day-care",
	# "veterinarian-emergency-services",
	# "kennels",
	# "mobile-pet-grooming",
	# "pet-boarding-kennels",
	# "pet-cemeteries-crematories",
	# "pet-grooming",
	# "veterinary-clinics-hospitals",

	# BEAUTY

	# "massage-therapists",
	# "barbers",
	# "nail-salons",
	# "beauty-supplies-equipment",
	# "hair-removal",
	# "hair-stylists",
	# "skin-care",
	# "beauty-salons",
	# "day-spas",
	# "hair-supplies-accessories,
]

list_of_urls = []

with open("yp_cities.txt", "r", encoding="utf-8") as cities_file:

    for line in cities_file:

        city = line.strip()
        state = city[-2:]

        if states_all or state in states:

            for category in categories:
                url = f"https://www.yellowpages.com/{city}/{category}"
                list_of_urls.append(url)

with open(output_file, "w", encoding="utf-8") as out_file:
    for url in list_of_urls:
        out_file.write(f"{url}\n")

print(f"Done, exported {len(list_of_urls)} URLs")
