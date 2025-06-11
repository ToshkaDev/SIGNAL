import pytest
from signalp.models import DomainStatisticsPerProtein
from factories import DomainStatisticsPerProteinFactory, GenomeMetadataFactory
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.postgres.indexes import GinIndex
from django.db.utils import DataError

@pytest.mark.django_db
def test_create_valid_instance():
    instance = DomainStatisticsPerProteinFactory()
    assert instance.mist_protein_accession.startswith("GCF_")
    assert instance.genome.genome_version == "GCF_000009965.1"

@pytest.mark.django_db
def test_unique_mist_protein_accession():
    DomainStatisticsPerProteinFactory(mist_protein_accession="GCF_000009965.1-TK_RS031251")
    with pytest.raises(IntegrityError):
        DomainStatisticsPerProteinFactory(mist_protein_accession="GCF_000009905.1-TK_RS03125199999")

@pytest.mark.django_db
def test_null_optional_fields():
    instance = DomainStatisticsPerProteinFactory(
        protein_length=None,
        domain_architecture=None,
        sensors_or_regulators=None,
        domain_counts=None,
        domains=None,
        search_vector=None
    )
    assert instance.protein_length is None
    assert instance.domain_architecture is None
    assert instance.protein_length is None
    assert instance.sensors_or_regulators is None
    assert instance.domain_counts is None
    assert instance.domains is None
    assert instance.search_vector is None

@pytest.mark.django_db
def test_foreign_key_relation():
    genome = GenomeMetadataFactory(genome_version="GCF_000009965.1")
    instance = DomainStatisticsPerProteinFactory(genome=genome)
    assert instance.genome.genome_version == "GCF_000009965.1"

@pytest.mark.django_db
def test_index_on_search_vector_exists():
    indexes = DomainStatisticsPerProtein._meta.indexes
    names = [idx.name for idx in indexes if idx.name]
    assert "search_vector_prot_idx" in names

@pytest.mark.django_db
def test_invalid_integer_field():
    with pytest.raises(ValueError):
        DomainStatisticsPerProteinFactory(
            protein_length="Cache",
            domain_counts="GPD"
        )

@pytest.mark.django_db
def test_json_field_serialization():
    data = {"domainA": 3, "domainB": 2}
    instance = DomainStatisticsPerProteinFactory(domain_counts=data)
    assert instance.domain_counts == data

@pytest.mark.django_db
def test_gin_index_on_domain_counts():
    indexes = DomainStatisticsPerProtein._meta.indexes
    assert any(isinstance(idx, GinIndex) and "domain_counts" in idx.fields for idx in indexes)

@pytest.mark.django_db
def test_invalid_protein_type_choice():
    obj = DomainStatisticsPerProteinFactory(protein_type="PAR")
    with pytest.raises(ValidationError):
        obj.full_clean()

@pytest.mark.django_db
def test_invalid_source_choice():
    obj = DomainStatisticsPerProteinFactory(source="UNKNOWN")
    with pytest.raises(ValidationError):
        obj.full_clean()

@pytest.mark.django_db
def test_max_length_enforcement():
    with pytest.raises(DataError):
        DomainStatisticsPerProteinFactory(mist_protein_accession="X" * 101)