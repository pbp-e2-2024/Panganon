import json
import os
from django.core.management.base import BaseCommand
from daftar_toko.models import Makanan

# python manage.py load_makanan dataset\Bika_Ambon_Medan dataset\Durian_Medan dataset\Kari_Medan dataset\Lontong_Medan dataser\Nasi_Lemak_Medan dataset\Sate_Medan dataset\Soto_Medan.json

class Command(BaseCommand):
    help = 'Load makanan data from multiple JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_paths',
            nargs='+',
            type=str,
            help='List of file paths to JSON datasets'
        )

    def handle(self, *args, **options):
        file_paths = options['file_paths']
        for file_path in file_paths:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for key, value in data.items():
                        Makanan.objects.create(
                            name=value['name'],
                            rating=value['rating'],
                            rating_amount=value['rating_amount'],
                            price_range=value.get('price_range'),
                            address=value['address'],
                            opening_hours=value['opening_hours'],
                            services=value['services'],
                            links=value['links'],
                            latitude=value['coordinates']['latitude'],
                            longitude=value['coordinates']['longitude'],
                        )
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {file_path}'))
            else:
                self.stdout.write(self.style.ERROR(f'File {file_path} does not exist'))