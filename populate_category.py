

import os
import sys
import django
from pathlib import Path

# Configura l'ambiente Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))  # ✅ Aggiunto per far trovare le app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DriveIsland.settings")  # Cambia se il tuo progetto ha un nome diverso
django.setup()

print("Popolamento categorie avviato...")

from cars.models import Category

categories = [
    {"name": "SUV", "description": "Sport Utility Vehicle, ideale per terreni difficili."},
    {"name": "Decappottabile", "description": "Auto con tetto apribile o rimovibile."},
    {"name": "Auto da corsa", "description": "Progettata per alte prestazioni e velocità."},
    {"name": "Utilitaria", "description": "Compatta ed economica, adatta alla città."},
    {"name": "Berlina", "description": "Comoda e spaziosa, adatta a viaggi lunghi."},
    {"name": "Station Wagon", "description": "Ampio bagagliaio, perfetta per le famiglie."},
    {"name": "Coupé", "description": "Design sportivo a due porte."},
    {"name": "Monovolume", "description": "Spaziosa e versatile per trasportare più passeggeri."},
    {"name": "Pickup", "description": "Cassone posteriore per trasporto merci leggere."},
    {"name": "Elettrica", "description": "Alimentata da motore elettrico, a basse emissioni."},
]

for cat in categories:
    obj, created = Category.objects.get_or_create(
        name=cat["name"],
        defaults={"description": cat["description"]}
    )
    if created:
        print(f"Categoria creata: {cat['name']}")
    else:
        print(f"Categoria già esistente: {cat['name']}")