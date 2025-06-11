import pytest
from signalp.models import DomainStatisticsPerGenome, Source, ProteinType, DomainCombinationType
from factories import DomainStatisticsPerGenomeFactory, GenomeMetadataFactory
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.utils import DataError

@pytest.mark.django_db
def test_create_valid_instance():
    instance = DomainStatisticsPerGenomeFactory()
    assert instance.genome_accession.startswith("GCF_")
    assert instance.genome.genome_version == "GCF_000009965.1"

@pytest.mark.django_db
def test_unique_together_constraint():
    base_instance = DomainStatisticsPerGenomeFactory(
        source=Source.MIST,
        protein_type=ProteinType.HK,
        domains="PAS_3,PAS_4,PAS_9",
        domain_combination_type=DomainCombinationType.domain_comb
    )
    with pytest.raises(IntegrityError):
        DomainStatisticsPerGenomeFactory(
            genome=base_instance.genome,
            source=base_instance.source,
            protein_type=base_instance.protein_type,
            domains=base_instance.domains,
            domain_combination_type=base_instance.domain_combination_type,
        )

@pytest.mark.django_db
def test_null_optional_fields():
    instance = DomainStatisticsPerGenomeFactory(
        genome_accession=None,
        domain_combination_type=None,
        count_raw=None,
        count_normalized_by_genome_size=None,
        count_normalized_by_total_proteins=None,
        search_vector=None
    )
    assert instance.genome_accession is None
    assert instance.domain_combination_type is None
    assert instance.count_raw is None
    assert instance.count_normalized_by_genome_size is None
    assert instance.count_normalized_by_total_proteins is None
    assert instance.search_vector is None

@pytest.mark.django_db
def test_foreign_key_relation():
    genome = GenomeMetadataFactory(genome_version="GCF_000009965.1")
    instance = DomainStatisticsPerGenomeFactory(genome=genome)
    assert instance.genome.genome_version == "GCF_000009965.1"

@pytest.mark.django_db
def test_index_on_search_vector_exists():
    indexes = DomainStatisticsPerGenome._meta.indexes
    names = [idx.name for idx in indexes if idx.name]
    assert "search_vector_genome_idx" in names

@pytest.mark.django_db
def test_invalid_decimal_field():
    with pytest.raises(ValidationError):
        DomainStatisticsPerGenomeFactory(
            count_normalized_by_genome_size="VWA",
        )

@pytest.mark.django_db
def test_invalid_integer_field():
    with pytest.raises(ValueError):
        DomainStatisticsPerGenomeFactory(
            count_raw="AA"
        )
        
@pytest.mark.django_db
def test_db_index_declared_on_field():
    field = DomainStatisticsPerGenome._meta.get_field("count_normalized_by_genome_size")
    assert field.db_index is True

@pytest.mark.django_db
def test_invalid_protein_type_choice():
    obj = DomainStatisticsPerGenomeFactory(protein_type="PAR")
    with pytest.raises(ValidationError):
        obj.full_clean()

@pytest.mark.django_db
def test_invalid_source_choice():
    obj = DomainStatisticsPerGenomeFactory(source="UNKNOWN")
    with pytest.raises(ValidationError):
        obj.full_clean()

@pytest.mark.django_db
def test_invalid_domaincombinationtype_choice():
    obj = DomainStatisticsPerGenomeFactory(domain_combination_type="class")
    with pytest.raises(ValidationError):
        obj.full_clean()

@pytest.mark.django_db
def test_max_length_enforcement():
    with pytest.raises(DataError):
        DomainStatisticsPerGenomeFactory(count_normalized_by_genome_size=1000.12345678)