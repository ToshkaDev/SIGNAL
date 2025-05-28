import csv
import logging
from pathlib import Path
from decimal import Decimal, InvalidOperation
from collections import defaultdict

from django.db import transaction
from signalp.models import DomainStatisticsPerTaxon, GenomeMetadata

logger = logging.getLogger(__name__)

FILE_PATH = Path(__file__).parent / "input" / "per_taxon_combined_db.tsv"

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

def load_domain_statistics_per_taxon(file_path=None, batch_size=1000):
    if file_path is None:
        file_path = FILE_PATH

    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File {file_path} does not exist")

    rows = []
    # gtdb_taxonomy_rank to gtdb_taxonomy_last dict to check in the genome metadta table for the presense of corresponding taxon entries before loading data
    rank_to_last = defaultdict(set)

    with file_path.open(newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row_num, row in enumerate(reader, start=1):
            gtdb_taxonomy_string = row.get("gtdb_taxonomy_string")
            gtdb_taxonomy_last = row.get("gtdb_taxonomy_last")
            gtdb_taxonomy_rank = row.get("gtdb_taxonomy_rank")
            source = row.get("source")
            protein_type = row.get("protein_type")
            domains = row.get("domains")
            domain_combination_type = row.get("domain_combination_type")

            if not gtdb_taxonomy_string or not source or not protein_type or not domains or not domain_combination_type:
                logger.warning(f"Skipping row {row_num} due to missing required fields: {row}")
                continue
            
            #taxonomy_lasts.add(gtdb_taxonomy_last)
            rank_to_last[gtdb_taxonomy_rank].add(gtdb_taxonomy_last)
            rows.append(row)

    # We are extracting GTDB taxonomy fields from the metadat table to ensure by comparision with this data that
    # all DomainStatisticsPerTaxon entries have taxons associated with them in the genome_metadata table (see below "Check existance" during loading data)
    taxons = set()
    existing_entries = set()
    for rank, last_taxons in rank_to_last.items():
        # to recreate the field name
        rank="gtdb_" + rank
        taxons.update(set(GenomeMetadata.objects.filter(**{f"{rank}__in": last_taxons}).values_list(rank, flat=True)))
        existing_entries.update(set(DomainStatisticsPerTaxon.objects.filter(gtdb_taxonomy_last__in=last_taxons)))

    existing_map = {
        (obj.gtdb_taxonomy_string, obj.source, obj.protein_type, obj.domains, obj.domain_combination_type): obj
        for obj in existing_entries
    }

    to_create = []
    to_update = []
    for row in rows:
        gtdb_taxonomy_last = row.get("gtdb_taxonomy_last")
        # Check existance: load records only if associated taxons are present in the genome_metadata table
        if not gtdb_taxonomy_last in taxons:
            logger.warning(f"Skipping row with unknown taxonomy: {row.get("gtdb_taxonomy_last")}")
            continue

        key = (row["gtdb_taxonomy_string"], row["source"], row["protein_type"], row["domains"], row["domain_combination_type"])
        defaults = {
            "gtdb_taxonomy_string": row.get("gtdb_taxonomy_string"),
            "gtdb_taxonomy_last": row.get("gtdb_taxonomy_last"),
            "gtdb_taxonomy_rank": row.get("gtdb_taxonomy_rank"),
            "source": row.get("source"),
            "protein_type": row.get("protein_type"),
            "domains": row.get("domains"),
            "domain_combination_type": row.get("domain_combination_type"),
            "count_raw": safe_int(row.get("count_raw")),
            "count_normalized_by_total_genomes": safe_decimal(row.get("count_normalized_by_total_genomes")),
            "count_normalized_by_genome_size_by_total_genomes": safe_decimal(row.get("count_normalized_by_genome_size_by_total_genomes")),
            "count_normalized_by_total_proteins_by_total_genomes": safe_decimal(row.get("count_normalized_by_total_proteins_by_total_genomes")),
        }

        if key in existing_map:
            obj = existing_map[key]
            for field, value in defaults.items():
                setattr(obj, field, value)
            to_update.append(obj)
        else:
            to_create.append(DomainStatisticsPerTaxon(**defaults))

    with transaction.atomic():
        for i in range(0, len(to_update), batch_size):
            DomainStatisticsPerTaxon.objects.bulk_update(
                to_update[i:i + batch_size],
                fields=[
                    "gtdb_taxonomy_string",
                    "gtdb_taxonomy_last",
                    "gtdb_taxonomy_rank",
                    "source",
                    "protein_type",
                    "domains",
                    "domain_combination_type",
                    "count_raw",
                    "count_normalized_by_total_genomes",
                    "count_normalized_by_genome_size_by_total_genomes",
                    "count_normalized_by_total_proteins_by_total_genomes",
                ]
            )

        for i in range(0, len(to_create), batch_size):
            DomainStatisticsPerTaxon.objects.bulk_create(to_create[i:i + batch_size])

    logger.info(f"Created {len(to_create)} new DomainStatisticsPerTaxon records")
    logger.info(f"Updated {len(to_update)} existing DomainStatisticsPerTaxon records")