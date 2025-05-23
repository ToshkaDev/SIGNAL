from django.core.management.base import BaseCommand
from signalp.loaders.per_genome_stats_loader import load_domain_statistics_per_genome

class Command(BaseCommand):
    help = 'Load genome metadata from a TSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=None,
            help='Path to the TSV file to load',
        )

    def handle(self, *args, **options):
        file_path = options['file']
        load_domain_statistics_per_genome(file_path=file_path)
        self.stdout.write(self.style.SUCCESS("Domain stats per genome loaded."))