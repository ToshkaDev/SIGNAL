import pytest
from rest_framework.test import APIClient
from factories import GenomeMetadataFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_genome_metadata_list_view(api_client):
    GenomeMetadataFactory()
    GenomeMetadataFactory(genome_version="GCF_000015765.1", gtdb_kingdom="Bacteria", ncbi_kingdom="Bacteria")

    response = api_client.get("/genomes/")
    assert response.status_code == 200
    print (response.data)
    assert len(response.data["results"]) == 2
    assert all("genome_version" in item for item in response.data["results"])

    # Test filtering
    response_filtered = api_client.get("/genomes/?genome_version=GCF_000015765.1")
    assert response_filtered.status_code == 200
    assert len(response_filtered.data["results"]) == 1
    assert response_filtered.data["results"][0]["genome_version"] == "GCF_000015765.1"

    # Test searching
    response_search = api_client.get("/genomes/?search=Archaea")
    assert response_search.status_code == 200
    assert len(response_search.data["results"]) == 1
    assert response_search.data["results"][0]["gtdb_kingdom"] == "Archaea"

@pytest.mark.django_db
def test_genome_metadata_detail_view(api_client):
    genome_metadata = GenomeMetadataFactory(genome_version="GCF_000015765.1")

    response = api_client.get(f"/genomes/{genome_metadata.pk}/")
    assert response.status_code == 200
    assert response.data["genome_version"] == "GCF_000015765.1"

    # Not existing genome
    response_404 = api_client.get("/genomes/1111111/")
    assert response_404.status_code == 404