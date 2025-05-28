from django.core.management.base import BaseCommand
from signalp.loaders.per_taxon_stats_loader import load_domain_statistics_per_taxon

class Command(BaseCommand):
    help = 'Load per taxon statistics from a TSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=None,
            help='Path to the TSV file to load',
        )

    def handle(self, *args, **options):
        file_path = options['file']
        load_domain_statistics_per_taxon(file_path=file_path)
        self.stdout.write(self.style.SUCCESS("Domain stats per taxon loaded."))