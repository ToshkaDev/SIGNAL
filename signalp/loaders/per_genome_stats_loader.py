import csv
import logging
from pathlib import Path
from decimal import Decimal, InvalidOperation

from django.db import transaction
from signalp.models import DomainStatisticsPerGenome, GenomeMetadata

logger = logging.getLogger(__name__)

FILE_PATH = Path(__file__).parent / "input" / "per_genome_combined_db.tsv"

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def safe_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError, TypeError):
        return None

def load_domain_statistics_per_genome(file_path=None, batch_size=1000):
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
            source = row.get("source")
            protein_type = row.get("protein_type")
            domains = row.get("domains")
            domain_combination_type = row.get("domain_combination_type")

            if not genome_version or not source or not protein_type or not domains or not domain_combination_type:
                logger.warning(f"Skipping row {row_num} due to missing required fields: {row}")
                continue
            
            genome_versions.add(genome_version)
            rows.append(row)

    # We extracting genome versions from the metadat table to ensure by comparision with this data that
    # all per_genome_stats entries have genomes associated with them in the genome_metadata table (see below "Check existance" during loading data)
    genome_map = {gm.genome_version: gm for gm in GenomeMetadata.objects.filter(genome_version__in=genome_versions)}
    existing_entires = DomainStatisticsPerGenome.objects.filter(genome__genome_version__in=genome_versions)
    existing_map = {
        (obj.genome.genome_version, obj.source, obj.protein_type, obj.domains, obj.domain_combination_type): obj
        for obj in existing_entires
    }

    to_create = []
    to_update = []

    for row in rows:
        genome = genome_map.get(row["genome"])
        # Check existance: load records only if associated genomes are present in the genome_metadata table
        if not genome:
            logger.warning(f"Skipping row with unknown genome: {row['genome']}")
            continue

        key = (row["genome"], row["source"], row["protein_type"], row["domains"], row["domain_combination_type"])
        defaults = {
            "genome": genome,
            "genome_accession": row.get("genome_accession"),
            "source": row.get("source"),
            "protein_type": row.get("protein_type"),
            "domains": row.get("domains"),
            "domain_combination_type": row.get("domain_combination_type"),
            "count_raw": safe_int(row.get("count_raw")),
            "count_normalized_by_genome_size": safe_decimal(row.get("count_normalized_by_genome_size")),
            "count_normalized_by_total_proteins": safe_decimal(row.get("count_normalized_by_total_proteins")),
        }

        if key in existing_map:
            obj = existing_map[key]
            for field, value in defaults.items():
                setattr(obj, field, value)
            to_update.append(obj)
        else:
            to_create.append(DomainStatisticsPerGenome(**defaults))

    with transaction.atomic():
        for i in range(0, len(to_update), batch_size):
            DomainStatisticsPerGenome.objects.bulk_update(
                to_update[i:i + batch_size],
                fields=[
                    "genome_accession",
                    "source",
                    "protein_type",
                    "domains",
                    "domain_combination_type",
                    "count_raw",
                    "count_normalized_by_genome_size",
                    "count_normalized_by_total_proteins",
                ]
            )

        for i in range(0, len(to_create), batch_size):
            DomainStatisticsPerGenome.objects.bulk_create(to_create[i:i + batch_size])

    logger.info(f"Created {len(to_create)} new DomainStatisticsPerGenome records")
    logger.info(f"Updated {len(to_update)} existing DomainStatisticsPerGenome records")