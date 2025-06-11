import csv
from django.core.management.base import BaseCommand
from language_app.models import Words


class Command(BaseCommand):
    help = 'CSV dosyasındaki verileri veritabanına aktarır'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV dosyasının yolu')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Words.objects.create(english=row[0], turkish=row[1])
        self.stdout.write(self.style.SUCCESS('CSV dosyasındaki veriler veritabanına başarıyla aktarıldı.'))
