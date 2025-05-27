from django.db import models
from django.db.models import F
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchQuery, SearchRank

class GenomeMetadata(models.Model):
    genome_version = models.CharField(max_length=100, unique=True)
    genome_accession = models.CharField(max_length=100, blank=True, null=True)
    genome_size = models.IntegerField(blank=True, null=True)
    protein_count = models.IntegerField(blank=True, null=True)

    # GTDB taxonomy
    gtdb_kingdom = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    gtdb_phylum = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    gtdb_class = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    gtdb_order = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    gtdb_family = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    gtdb_genus = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    gtdb_species = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    # NCBI taxonomy
    ncbi_kingdom = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ncbi_phylum = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ncbi_class = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ncbi_order = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ncbi_family = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ncbi_genus = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ncbi_species = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    def __str__(self):
        return self.genome_version

class ProteinType(models.TextChoices):
    HK = 'hk', 'Histidine Kinase'
    RR = 'rr', 'Response Regulator'
    OCP = 'ocp', 'One-Component System'

class Source(models.TextChoices):
    MIST = 'mistdb', 'MiST database'
    RMODELS = 'rmodels', 'Pfam models with relaxed thresholds'

class FullTextSearchQuerySet(models.QuerySet):
    def search(self, query_string):
        query = SearchQuery(query_string)
        return self.annotate(rank=SearchRank(F('search_vector'), query)).filter(search_vector=query).order_by('-rank')

class DomainStatisticsPerProtein(models.Model):
    genome = models.ForeignKey(GenomeMetadata, to_field='genome_version', on_delete=models.CASCADE)
    genome_accession = models.CharField(max_length=100, blank=True, null=True)
    ncbi_protein_accession = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    mist_protein_accession = models.CharField(max_length=100, unique=True, db_index=True)
    protein_type = models.CharField(max_length=3, choices=ProteinType.choices, db_index=True)
    source =  models.CharField(max_length=7, choices=Source.choices, db_index=True)
    protein_length = models.IntegerField(blank=True, null=True)
    domain_architecture = models.TextField(blank=True, null=True)
    sensors_or_regulators = models.TextField(blank=True, null=True)
    domain_counts = models.JSONField(blank=True, null=True, db_index=True)
    domains = models.TextField(blank=True, null=True)
    search_vector = SearchVectorField(blank=True, null=True)
    objects = FullTextSearchQuerySet.as_manager()

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'], name='search_vector_prot_idx'),
            GinIndex(fields=['domain_counts'])
        ]

    def __str__(self):
        return self.mist_protein_accession

class DomainCombinationType(models.TextChoices):
    domain = 'domain'
    domain_comb = 'domain_comb'
    superfamily = 'superfamily'
    superfamily_comb = 'superfamily_comb'

class DomainStatisticsPerGenome(models.Model):
    genome = models.ForeignKey(GenomeMetadata, to_field='genome_version', on_delete=models.CASCADE)
    genome_accession = models.CharField(max_length=100, blank=True, null=True)
    source =  models.CharField(max_length=7, choices=Source.choices, db_index=True)
    protein_type = models.CharField(max_length=3, choices=ProteinType.choices, db_index=True)
    domains = models.TextField()
    domain_combination_type = models.TextField(blank=True, null=True, choices=DomainCombinationType.choices, db_index=True)
    count_raw = models.IntegerField(blank=True, null=True, db_index=True)
    count_normalized_by_genome_size = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, db_index=True)
    count_normalized_by_total_proteins = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, db_index=True)
    search_vector = SearchVectorField(blank=True, null=True)
    objects = FullTextSearchQuerySet.as_manager()

    class Meta:
        unique_together = ('genome', 'source', 'protein_type', 'domains', 'domain_combination_type')
        indexes = [
            GinIndex(fields=['search_vector'], name='search_vector_genome_idx')
        ]

class DomainStatisticsPerTaxon(models.Model):
    gtdb_taxonomy_string = models.TextField()
    gtdb_taxonomy_last = models.CharField(max_length=100, db_index=True)
    gtdb_taxonomy_rank = models.CharField(max_length=20, blank=True, null=True)
    source =  models.CharField(max_length=7, choices=Source.choices, db_index=True)
    protein_type = models.CharField(max_length=3, choices=ProteinType.choices, db_index=True)
    domains = models.TextField()
    domain_combination_type = models.TextField(blank=True, null=True, choices=DomainCombinationType.choices, db_index=True)
    count_raw = models.IntegerField(blank=True, null=True, db_index=True)
    count_normalized_by_total_genomes = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, db_index=True)
    count_normalized_by_genome_size_by_total_genomes = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, db_index=True)
    count_normalized_by_total_proteins_by_total_genomes = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, db_index=True)
    search_vector = SearchVectorField(blank=True, null=True)
    objects = FullTextSearchQuerySet.as_manager()

    genomes = models.ManyToManyField(
        "GenomeMetadata",
        through="TaxonGenomeLink",
        related_name="mist_taxon_statistics"
    )

    class Meta:
        unique_together = ('gtdb_taxonomy_string', 'protein_type', 'domains')
        indexes = [
            GinIndex(fields=['search_vector'], name='search_vector_taxon_idx')
        ]

class TaxonGenomeLink(models.Model):
    taxon = models.ForeignKey(DomainStatisticsPerTaxon, on_delete=models.CASCADE)
    genome = models.ForeignKey(GenomeMetadata, on_delete=models.CASCADE)