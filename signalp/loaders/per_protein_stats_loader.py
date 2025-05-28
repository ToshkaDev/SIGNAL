import csv
import logging
from pathlib import Path
from decimal import Decimal, InvalidOperation

from django.db import transaction
from signalp.models import DomainStatisticsPerProtein, GenomeMetadata

logger = logging.getLogger(__name__)

FILE_PATH = Path(__file__).parent / "input" / "per_protein_combined_db.tsv"

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def load_domain_statistics_per_protein(file_path=None, batch_size=1000):
    if file_path is None:
        file_path = FILE_PATH

    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File {file_path} does not exist")

    rows = []
    genome_versions = set()

    with file_path.open(newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row_num, row in enumerate(reader, start=1):
            genome_version = row.get("genome")
            mist_protein_accession = row.get("mist_protein_accession")
            source = row.get("source")
            protein_type = row.get("protein_type")

            if not mist_protein_accession or not genome_version or not source or not protein_type:
                logger.warning(f"Skipping row {row_num} due to missing required fields: {row}")
                continue

            genome_versions.add(genome_version)
            rows.append(row)

    # We are extracting genome versions from the metadat table to ensure by comparision with this data that
    # all DomainStatisticsPerProtein entries have genomes associated with them in the genome_metadata table (see below "Check existance" during loading data)
    genome_map = {gm.genome_version: gm for gm in GenomeMetadata.objects.filter(genome_version__in=genome_versions)}
    existing_entries = DomainStatisticsPerProtein.objects.filter(genome__genome_version__in=genome_versions)
    existing_map = { obj.mist_protein_accession: obj for obj in existing_entries }

    to_create = []
    to_update = []

    for row in rows:
        genome = genome_map.get(row["genome"])
        # Check existance: load records only if associated genomes are present in the genome_metadata table
        if not genome:
            logger.warning(f"Skipping row with unknown genome: {row['genome']}")
            continue

        mist_protein_accession = row.get('mist_protein_accession')
        defaults = {
            "genome": genome,
            "genome_accession": row.get("genome_accession"),
            "ncbi_protein_accession": row.get("ncbi_protein_accession"),
            "mist_protein_accession": row.get("mist_protein_accession"),
            "protein_type": row.get("protein_type"),
            "source": row.get("source"),
            "protein_length": safe_int(row.get("protein_length")),
            "domain_architecture": row.get("domain_architecture"),
            "sensors_or_regulators": row.get("sensors_or_regulators"),
            "domain_counts": row.get("domain_counts"),
            "domains": row.get("domains"),
        }

        if mist_protein_accession in existing_map:
            obj = existing_map[mist_protein_accession]
            for field, value in defaults.items():
                setattr(obj, field, value)
            to_update.append(obj)
        else:
            to_create.append(DomainStatisticsPerProtein(**defaults))

    with transaction.atomic():
        for i in range(0, len(to_update), batch_size):
            DomainStatisticsPerProtein.objects.bulk_update(
                to_update[i:i + batch_size],
                fields=[
                    "genome",
                    "genome_accession",
                    "ncbi_protein_accession",
                    "mist_protein_accession",
                    "protein_type",
                    "source",
                    "protein_length",
                    "domain_architecture",
                    "sensors_or_regulators",
                    "domain_counts",
                    "domains",
                ],
            )

        for i in range(0, len(to_create), batch_size):
            DomainStatisticsPerProtein.objects.bulk_create(to_create[i:i + batch_size])

    logger.info(f"Created {len(to_create)} new DomainStatisticsPerProtein records")
    logger.info(f"Updated {len(to_update)} existing DomainStatisticsPerProtein records")