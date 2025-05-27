import csv
import logging
from pathlib import Path

from django.db import transaction
from signalp.models import GenomeMetadata

logger = logging.getLogger(__name__)

FILE_PATH = Path(__file__).parent / "input" / "ar_bac_metadata_r214_db.tsv"


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def load_genome_metadata_from_tsv(file_path=None, batch_size=1000):
    """
    Load or update GenomeMetadata entries from a TSV file.
    Args:
        file_path (Path or str): Path to the TSV file.
        batch_size (int): Number of records per batch for bulk ops.
    """
    if file_path is None:
        file_path = FILE_PATH

    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File {file_path} does not exist")

    rows = []
    genome_versions = set()

    # Read all rows first
    with file_path.open(newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row_num, row in enumerate(reader, start=1):
            genome_version = row.get('genome_version')
            if not genome_version:
                logger.warning(f"Skipping row {row_num} without genome_version: {row}")
                continue
            genome_versions.add(genome_version)
            rows.append(row)

    # Fetch existing GenomeMetadata records
    existing_gs = GenomeMetadata.objects.filter(genome_version__in=genome_versions)
    existing_map = {gm.genome_version: gm for gm in existing_gs}

    to_create = []
    to_update = []

    for row_num, row in enumerate(rows, start=1):
        genome_version = row['genome_version']

        defaults = {
            'genome_accession': row.get('genome_accession'),
            'genome_size': safe_int(row.get('genome_size')),
            'protein_count': safe_int(row.get('protein_count')),
            'gtdb_kingdom': row.get('gtdb_kingdom'),
            'gtdb_phylum': row.get('gtdb_phylum'),
            'gtdb_class': row.get('gtdb_class'),
            'gtdb_order': row.get('gtdb_order'),
            'gtdb_family': row.get('gtdb_family'),
            'gtdb_genus': row.get('gtdb_genus'),
            'gtdb_species': row.get('gtdb_species'),
            'ncbi_kingdom': row.get('ncbi_kingdom'),
            'ncbi_phylum': row.get('ncbi_phylum'),
            'ncbi_class': row.get('ncbi_class'),
            'ncbi_order': row.get('ncbi_order'),
            'ncbi_family': row.get('ncbi_family'),
            'ncbi_genus': row.get('ncbi_genus'),
            'ncbi_species': row.get('ncbi_species'),
        }

        if genome_version in existing_map:
            # Update existing object fields
            gm = existing_map[genome_version]
            for key, val in defaults.items():
                setattr(gm, key, val)
            to_update.append(gm)
        else:
            # Create new instance
            gm = GenomeMetadata(genome_version=genome_version, **defaults)
            to_create.append(gm)

    with transaction.atomic():
        # Bulk update existing records in batches
        for i in range(0, len(to_update), batch_size):
            GenomeMetadata.objects.bulk_update(
                to_update[i : i + batch_size],
                fields=[
                    'genome_accession',
                    'genome_size',
                    'protein_count',
                    'gtdb_kingdom',
                    'gtdb_phylum',
                    'gtdb_class',
                    'gtdb_order',
                    'gtdb_family',
                    'gtdb_genus',
                    'gtdb_species',
                    'ncbi_kingdom',
                    'ncbi_phylum',
                    'ncbi_class',
                    'ncbi_order',
                    'ncbi_family',
                    'ncbi_genus',
                    'ncbi_species',
                ],
            )

        # Bulk create new records in batches
        for i in range(0, len(to_create), batch_size):
            GenomeMetadata.objects.bulk_create(to_create[i : i + batch_size])

    logger.info(f"Created {len(to_create)} new GenomeMetadata records")
    logger.info(f"Updated {len(to_update)} existing GenomeMetadata records")
