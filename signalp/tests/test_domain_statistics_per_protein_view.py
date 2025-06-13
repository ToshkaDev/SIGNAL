import pytest
from rest_framework.test import APIClient
from factories import DomainStatisticsPerProteinFactory, GenomeMetadataFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_domain_stats_per_protein_list_view(api_client):
    genome_metadata1 = GenomeMetadataFactory(genome_version="GCF_000009965.1")
    DomainStatisticsPerProteinFactory(genome=genome_metadata1, domain_architecture="Response_reg:4-115", mist_protein_accession="GCF_000009965.1-TK_RS031251")
    genome_metadata2 = GenomeMetadataFactory(genome_version="GCF_000015765.1")
    DomainStatisticsPerProteinFactory(genome=genome_metadata2, domain_architecture="Cache:2-205,GAF:210-400", mist_protein_accession="GCF_000015765.1-MLAB_RS06235")

    response = api_client.get("/protein-stats/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 2
    assert all("genome" in item for item in response.data["results"])

    # Test filtering
    response_filtered = api_client.get("/protein-stats/?genome=GCF_000015765.1")
    assert response_filtered.status_code == 200
    assert len(response_filtered.data["results"]) == 1
    assert response_filtered.data["results"][0]["genome"] == "GCF_000015765.1"

    # Test searching
    response_search = api_client.get("/protein-stats/?search=Cache")
    assert response_search.status_code == 200
    assert len(response_search.data["results"]) == 1
    assert response_search.data["results"][0]["domain_architecture"] == "Cache:2-205,GAF:210-400"

@pytest.mark.django_db
def test_domain_stats_per_protein_detail_view(api_client):
    genome_metadata = GenomeMetadataFactory(genome_version="GCF_000015765.1")
    domain_stats_per_protein = DomainStatisticsPerProteinFactory(genome=genome_metadata)

    response = api_client.get(f"/protein-stats/{domain_stats_per_protein.pk}/")
    assert response.status_code == 200
    assert response.data["genome"] == "GCF_000015765.1"

    # Not existing genome
    response_404 = api_client.get("/protein-stats/1111111/")
    assert response_404.status_code == 404