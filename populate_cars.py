# populate_cars.py
import os
import sys
import django
from pathlib import Path
from django.core.files import File

# Configura l'ambiente Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))  # ✅ Aggiunto per far trovare le app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DriveIsland.settings")  # Cambia se il tuo progetto ha un nome diverso
django.setup()

from cars.models import Car, Category

# Percorso assoluto dell’immagine esistente
image_path = Path(__file__).resolve().parent / 'media/cars/audi-a4-avant/0b9d469c-479f-4142-a3db-6ba38e9ec739.jpg'

if not image_path.exists():
    print(f"❌ Immagine non trovata: {image_path}")
    exit()

with open(image_path, 'rb') as img_file:
    img = File(img_file, name= 'panda.jpg')

    with open(image_path, 'rb') as f4:
        Car.objects.create(
            model="Peugeot 208 BlueHDi",
            image_principal=File(f4, name='mercedes-a.jpg'),
            price_per_day=42.00,
            fuel_type="diesel",
            gearbox="manuale",
            category=Category.objects.get(name="SUV"),
            air_conditioning=True,
            color="Blu"
        )

    # Auto 5
    with open(image_path, 'rb') as f5:
        Car.objects.create(
            model="Ford Focus EcoBoost",
            image_principal=File(f5, name='focus.jpg'),
            price_per_day=48.00,
            fuel_type="benzina",
            gearbox="manuale",
            category=Category.objects.get(name="Decappottabile"),
            air_conditioning=True,
            color="Nero"
        )

    # Auto 6
    with open(image_path, 'rb') as f6:
        Car.objects.create(
            model="Panda 1.2",
            image_principal=File(f6, name='yaris.jpg'),
            price_per_day=45.00,
            fuel_type="ibrido",
            gearbox="automatico",
            category=Category.objects.get(name="Berlina"),
            air_conditioning=True,
            color="Rosso metallizzato"
        )

    with open(image_path, 'rb') as f7:
        Car.objects.create(
            model="Lamborghini",
            image_principal=File(f7, name='yaris.jpg'),
            price_per_day=45.00,
            fuel_type="ibrido",
            gearbox="automatico",
            category=Category.objects.get(name="Berlina"),
            air_conditioning=True,
            color="Rosso metallizzato"
        )

    with open(image_path, 'rb') as f8:
        Car.objects.create(
            model="Mehary",
            image_principal=File(f8, name='yaris.jpg'),
            price_per_day=45.00,
            fuel_type="ibrido",
            gearbox="automatico",
            category=Category.objects.get(name="Berlina"),
            air_conditioning=True,
            color="Rosso metallizzato"
        )

    with open(image_path, 'rb') as f9:
        Car.objects.create(
            model="Mehary",
            image_principal=File(f9, name='yaris.jpg'),
            price_per_day=45.00,
            fuel_type="ibrido",
            gearbox="automatico",
            category=Category.objects.get(name="Berlina"),
            air_conditioning=True,
            color="Rosso metallizzato"
        )

    with open(image_path, 'rb') as f10:
        Car.objects.create(
            model="Mehary",
            image_principal=File(f10, name='yaris.jpg'),
            price_per_day=45.00,
            fuel_type="ibrido",
            gearbox="automatico",
            category=Category.objects.get(name="Berlina"),
            air_conditioning=True,
            color="Rosso metallizzato"
        )


print("✅ Auto inserite con successo!")
