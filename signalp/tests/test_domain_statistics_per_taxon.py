import pytest
from signalp.models import DomainStatisticsPerTaxon, TaxonGenomeLink, Source, ProteinType, DomainCombinationType
from factories import DomainStatisticsPerTaxonFactory, GenomeMetadataFactory
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.utils import DataError

@pytest.mark.django_db
def test_create_valid_instance():
    instance = DomainStatisticsPerTaxonFactory()
    assert instance.gtdb_taxonomy_string.startswith("Archaea;")
    assert instance.gtdb_taxonomy_last == "Methanomicrobiales"

@pytest.mark.django_db
def test_unique_together_constraint():
    base_instance = DomainStatisticsPerTaxonFactory(
        gtdb_taxonomy_string="Archaea;Halobacteriota;Methanomicrobia;Methanomicrobiales",
        source=Source.MIST,
        protein_type=ProteinType.HK,
        domains="PAS_Fold,PAS_Fold,Peripla_BP",
        domain_combination_type=DomainCombinationType.domain_comb
    )
    with pytest.raises(IntegrityError):
        DomainStatisticsPerTaxonFactory(
            gtdb_taxonomy_string=base_instance.gtdb_taxonomy_string,
            source=base_instance.source,
            protein_type=base_instance.protein_type,
            domains=base_instance.domains,
            domain_combination_type=base_instance.domain_combination_type,
        )

@pytest.mark.django_db
def test_null_optional_fields():
    instance = DomainStatisticsPerTaxonFactory(
        gtdb_taxonomy_rank=None,
        domain_combination_type=None,
        count_raw=None,
        count_normalized_by_total_genomes=None,
        count_normalized_by_genome_size_by_total_genomes=None,
        count_normalized_by_total_proteins_by_total_genomes=None,
        search_vector=None
    )
    assert instance.gtdb_taxonomy_rank is None
    assert instance.domain_combination_type is None
    assert instance.count_raw is None
    assert instance.count_normalized_by_total_genomes is None
    assert instance.count_normalized_by_genome_size_by_total_genomes is None
    assert instance.count_normalized_by_total_proteins_by_total_genomes is None
    assert instance.search_vector is None

@pytest.mark.django_db
def test_m2m_domain_statistics_to_genome_relationship():
    # Create two GenomeMetadata instances
    genome_metadata1 = GenomeMetadataFactory(genome_version="GCF_000013445.1")
    genome_metadata2 = GenomeMetadataFactory(genome_version="GCF_000015765.1")

    domain_stat_per_taxon = DomainStatisticsPerTaxonFactory()

    # Link the domain_stat_per_taxon to GenomeMetadata instances via the through model
    TaxonGenomeLink.objects.create(taxon=domain_stat_per_taxon, genome=genome_metadata1)
    TaxonGenomeLink.objects.create(taxon=domain_stat_per_taxon, genome=genome_metadata2)

    # Assert the many-to-many relation from DomainStatisticsPerTaxon to GenomeMetadata
    linked_genomes = domain_stat_per_taxon.genomes.all()
    assert genome_metadata1 in linked_genomes
    assert genome_metadata2 in linked_genomes
    assert linked_genomes.count() == 2

    # Assert the reverse relation from GenomeMetadata to DomainStatisticsPerTaxon
    linked_taxons = genome_metadata1.mist_taxon_statistics.all()
    assert domain_stat_per_taxon in linked_taxons

@pytest.mark.django_db
def test_index_on_search_vector_exists():
    indexes = DomainStatisticsPerTaxon._meta.indexes
    names = [idx.name for idx in indexes if idx.name]
    assert "search_vector_taxon_idx" in names

@pytest.mark.django_db
def test_invalid_decimal_field():
    with pytest.raises(ValidationError):
        DomainStatisticsPerTaxonFactory(
            count_normalized_by_total_proteins_by_total_genomes="VWA",
        )

@pytest.mark.django_db
def test_invalid_integer_field():
    with pytest.raises(ValueError):
        DomainStatisticsPerTaxonFactory(
            count_raw="AA",
        )
        
@pytest.mark.django_db
def test_db_index_declared_on_field():
    field = DomainStatisticsPerTaxon._meta.get_field("gtdb_taxonomy_last")
    assert field.db_index is True

@pytest.mark.django_db
def test_invalid_protein_type_choice():
    obj = DomainStatisticsPerTaxonFactory(protein_type="PAR")
    with pytest.raises(ValidationError):
        obj.full_clean()

@pytest.mark.django_db
def test_invalid_source_choice():
    obj = DomainStatisticsPerTaxonFactory(source="UNKNOWN")
    with pytest.raises(ValidationError):
        obj.full_clean()

@pytest.mark.django_db
def test_invalid_domaincombinationtype_choice():
    obj = DomainStatisticsPerTaxonFactory(domain_combination_type="group")
    with pytest.raises(ValidationError):
        obj.full_clean()

@pytest.mark.django_db
def test_max_length_enforcement():
    with pytest.raises(DataError):
        DomainStatisticsPerTaxonFactory(count_normalized_by_total_proteins_by_total_genomes=1010.12345678)