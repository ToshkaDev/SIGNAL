import pytest
from rest_framework.test import APIClient
from factories import DomainStatisticsPerGenomeFactory, GenomeMetadataFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_genome_metadata_list_view(api_client):
    genome_metadata1 = GenomeMetadataFactory(genome_version="GCF_000009965.1")
    DomainStatisticsPerGenomeFactory(genome=genome_metadata1, domains="PAS_3,PAS_4,PAS_9", count_normalized_by_genome_size=4.882401262588967e-07)
    genome_metadata2 = GenomeMetadataFactory(genome_version="GCF_000015765.1")
    DomainStatisticsPerGenomeFactory(genome=genome_metadata2, domains="GAF_2,GAF_3,PAS_3,PAS_4", count_normalized_by_genome_size=1.8468846442007515e-06)

    response = api_client.get("/genome-stats/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 2
    assert all("genome" in item for item in response.data["results"])

    # Test filtering
    response_filtered = api_client.get("/genome-stats/?count_normalized_by_genome_size__lte=1.7468846442007515e-06")
    assert response_filtered.status_code == 200
    print (response_filtered.data)
    assert len(response_filtered.data["results"]) == 1
    # count_normalized_by_genome_size field forces this 4.882401262588967e-07 (set in the factory) to become this: 0.000000488
    assert response_filtered.data["results"][0]["count_normalized_by_genome_size"] == '0.000000488'

    # Test searching
    response_search = api_client.get("/genome-stats/?search=GAF")
    assert response_search.status_code == 200
    assert len(response_search.data["results"]) == 1
    assert response_search.data["results"][0]["domains"] == "GAF_2,GAF_3,PAS_3,PAS_4"

@pytest.mark.django_db
def test_genome_metadata_detail_view(api_client):
    genome_metadata = GenomeMetadataFactory(genome_version="GCF_000015765.1")
    domain_stats_per_genome = DomainStatisticsPerGenomeFactory(genome=genome_metadata)

    response = api_client.get(f"/genome-stats/{domain_stats_per_genome.pk}/")
    assert response.status_code == 200
    assert response.data["genome"] == "GCF_000015765.1"

    # Not existing genome
    response_404 = api_client.get("/genome-stats/1111111/")
    assert response_404.status_code == 404