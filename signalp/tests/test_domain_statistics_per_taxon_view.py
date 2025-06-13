import pytest
from rest_framework.test import APIClient
from factories import DomainStatisticsPerTaxonFactory, GenomeMetadataFactory
from signalp.models import TaxonGenomeLink

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_domain_stats_per_taxon_list_view(api_client):
        # Create two GenomeMetadata instances
    genome_metadata1 = GenomeMetadataFactory(genome_version="GCF_000013445.1")
    genome_metadata2 = GenomeMetadataFactory(genome_version="GCF_000009965.1")
    domain_stat_per_taxon1 = DomainStatisticsPerTaxonFactory(gtdb_taxonomy_string="Archaea;Halobacteriota;Methanomicrobia;Methanomicrobiales", gtdb_taxonomy_last="Methanomicrobiales", count_normalized_by_total_genomes=1.7468846442007515e-06)

    genome_metadata3 = GenomeMetadataFactory(genome_version="GCA_001800075.1")
    genome_metadata4 = GenomeMetadataFactory(genome_version="GCA_001800185.1")
    domain_stat_per_taxon2 = DomainStatisticsPerTaxonFactory(gtdb_taxonomy_string="Bacteria;Elusimicrobiota;Elusimicrobia", gtdb_taxonomy_last="Elusimicrobia", count_normalized_by_total_genomes=1.7468846442007515e-03)

    # Link the domain_stat_per_taxon to GenomeMetadata instances via the through model
    TaxonGenomeLink.objects.create(taxon=domain_stat_per_taxon1, genome=genome_metadata1)
    TaxonGenomeLink.objects.create(taxon=domain_stat_per_taxon1, genome=genome_metadata2)

    TaxonGenomeLink.objects.create(taxon=domain_stat_per_taxon2, genome=genome_metadata3)
    TaxonGenomeLink.objects.create(taxon=domain_stat_per_taxon2, genome=genome_metadata4)


    response = api_client.get("/taxon-stats/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 2
    assert all("gtdb_taxonomy_string" in item for item in response.data["results"])

    # Test filtering
    response_filtered = api_client.get("/taxon-stats/?count_normalized_by_total_genomes__gte=1.7468846442007515e-03")
    assert response_filtered.status_code == 200
    print (response_filtered.data)
    assert len(response_filtered.data["results"]) == 1
    # count_normalized_by_genome_size field forces this 1.7468846442007515e-03 (set in the factory) to become this: 0.0017469
    assert response_filtered.data["results"][0]["count_normalized_by_total_genomes"] == '0.0017469'

    # Test searching
    response_search = api_client.get("/taxon-stats/?search=Elusimicrobia")
    assert response_search.status_code == 200
    assert len(response_search.data["results"]) == 1
    print (response_search.data)
    assert response_search.data["results"][0]["gtdb_taxonomy_string"] == "Bacteria;Elusimicrobiota;Elusimicrobia"
    # Test linked genome_metadata models
    assert len(response_search.data["results"][0]["genomes"]) == 2

@pytest.mark.django_db
def test_domain_stats_per_taxon_detail_view(api_client):
    genome_metadata1 = GenomeMetadataFactory(genome_version="GCF_000013445.1")
    genome_metadata2 = GenomeMetadataFactory(genome_version="GCF_000009965.1")
    domain_stat_per_taxon = DomainStatisticsPerTaxonFactory(gtdb_taxonomy_string="Archaea;Halobacteriota;Methanomicrobia;Methanomicrobiales", count_normalized_by_total_genomes=1.7468846442007515e-06)
    TaxonGenomeLink.objects.create(taxon=domain_stat_per_taxon, genome=genome_metadata1)
    TaxonGenomeLink.objects.create(taxon=domain_stat_per_taxon, genome=genome_metadata2)

    response = api_client.get(f"/taxon-stats/{domain_stat_per_taxon.pk}/")
    assert response.status_code == 200
    assert response.data["gtdb_taxonomy_string"] == "Archaea;Halobacteriota;Methanomicrobia;Methanomicrobiales"

    # Not existing domain_stat_per_taxon
    response_404 = api_client.get("/taxon-stats/1111111/")
    assert response_404.status_code == 404