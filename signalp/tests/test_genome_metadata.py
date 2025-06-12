import pytest
from signalp.models import GenomeMetadata
from factories import GenomeMetadataFactory
from django.db import IntegrityError
from django.db.utils import DataError

@pytest.mark.django_db
def test_create_valid_instance():
    instance = GenomeMetadataFactory()
    assert instance.genome_version == "GCF_000009965.1"

@pytest.mark.django_db
def test_unique_genome_versionn():
    GenomeMetadataFactory(genome_version="GCF_000009965.1")
    with pytest.raises(IntegrityError):
        GenomeMetadataFactory(genome_version="GCF_000009965.1")

@pytest.mark.django_db
def test_null_optional_fields():
    instance = GenomeMetadataFactory(
        genome_accession=None,
        genome_size=None,
        protein_count=None,
        gtdb_kingdom=None,
        gtdb_phylum=None,
        gtdb_class=None,
        gtdb_order=None,
        gtdb_genus=None,
        gtdb_species=None,
        ncbi_kingdom=None,
        ncbi_phylum=None,
        ncbi_class=None,
        ncbi_order=None,
        ncbi_genus=None,
        ncbi_species=None,
    )
    assert instance.genome_accession is None
    assert instance.genome_size is None
    assert instance.protein_count is None
    assert instance.gtdb_kingdom is None
    assert instance.gtdb_phylum is None
    assert instance.gtdb_class is None
    assert instance.gtdb_order is None
    assert instance.gtdb_genus is None
    assert instance.gtdb_species is None
    assert instance.ncbi_kingdom is None
    assert instance.ncbi_phylum is None
    assert instance.ncbi_class is None
    assert instance.ncbi_order is None
    assert instance.ncbi_genus is None
    assert instance.ncbi_species is None

@pytest.mark.django_db
def test_db_index_declared_on_field():
    field = GenomeMetadata._meta.get_field("gtdb_kingdom")
    assert field.db_index is True

@pytest.mark.django_db
def test_invalid_integer_field():
    with pytest.raises(ValueError):
        GenomeMetadataFactory(
            genome_size="Big",
            protein_count="GPD",
        )

@pytest.mark.django_db
def test_max_length_enforcement():
    with pytest.raises(DataError):
        GenomeMetadataFactory(gtdb_kingdom="X" * 101)