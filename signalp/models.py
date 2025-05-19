from django.db import models

class GenomeMetadata(models.Model):
    genome_version = models.CharField(max_length=100, unique=True)
    genome_accession = models.CharField(max_length=100, blank=True, null=True)
    genome_size = models.IntegerField(blank=True, null=True)
    protein_count = models.IntegerField(blank=True, null=True)

    # GTDB taxonomy
    gtdb_kingdom = models.CharField(max_length=100, blank=True, null=True)
    gtdb_phylum = models.CharField(max_length=100, blank=True, null=True)
    gtdb_class = models.CharField(max_length=100, blank=True, null=True)
    gtdb_order = models.CharField(max_length=100, blank=True, null=True)
    gtdb_family = models.CharField(max_length=100, blank=True, null=True)
    gtdb_genus = models.CharField(max_length=100, blank=True, null=True)
    gtdb_species = models.CharField(max_length=100, blank=True, null=True)

    # NCBI taxonomy
    ncbi_kingdom = models.CharField(max_length=100, blank=True, null=True)
    ncbi_phylum = models.CharField(max_length=100, blank=True, null=True)
    ncbi_class = models.CharField(max_length=100, blank=True, null=True)
    ncbi_order = models.CharField(max_length=100, blank=True, null=True)
    ncbi_family = models.CharField(max_length=100, blank=True, null=True)
    ncbi_genus = models.CharField(max_length=100, blank=True, null=True)
    ncbi_species = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.genome_version


class ProteinType(models.TextChoices):
    HK = 'HK', 'Histidine Kinase'
    RR = 'rr', 'Response Regulator'
    OCS = 'ocs', 'One-Component System'

class Source(models.TextChoices):
    MIST = 'mist', 'MiST database'
    RMODELS = 'rmodels', 'Pfam models with relaxed thresholds'

class DomainStatisticsPerProtein(models.Model):
    genome = models.ForeignKey(GenomeMetadata, to_field='genome_version', on_delete=models.CASCADE)
    genome_accession = models.CharField(max_length=100, blank=True, null=True)
    ncbi_protein_accession = models.CharField(max_length=100, blank=True, null=True)
    mist_protein_accession = models.CharField(max_length=100, unique=True)
    protein_type = models.CharField(max_length=3, choices=ProteinType.choices)
    source =  models.CharField(max_length=7, choices=Source.choices)
    protein_length = models.IntegerField(blank=True, null=True)
    domain_architecture = models.TextField(blank=True, null=True)
    sensors_or_regulators = models.TextField(blank=True, null=True)
    domain_counts = models.JSONField(blank=True, null=True)
    domain_combination = models.JSONField(blank=True, null=True)

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
    source =  models.CharField(max_length=7, choices=Source.choices)
    protein_type = models.CharField(max_length=3, choices=ProteinType.choices)
    domains = models.TextField()
    domain_combination_type = models.TextField(blank=True, null=True, choices=DomainCombinationType.choices)
    count_raw = models.IntegerField(blank=True, null=True)
    count_normalized_by_genome_size = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    count_normalized_by_total_proteins = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)

    class Meta:
        unique_together = ('genome', 'protein_type', 'domains')


class DomainStatisticsPerTaxon(models.Model):
    gtdb_taxonomy_string = models.TextField()
    gtdb_taxonomy_last = models.CharField(max_length=100)
    gtdb_taxonomy_rank = models.CharField(max_length=20, blank=True, null=True)
    source =  models.CharField(max_length=7, choices=Source.choices)
    protein_type = models.CharField(max_length=3, choices=ProteinType.choices)
    domains = models.TextField()
    domain_combination_type = models.TextField(blank=True, null=True)
    count_raw = models.IntegerField(blank=True, null=True)
    count_normalized_by_total_genomes = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    count_normalized_by_genome_size_by_total_genomes = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    count_normalized_by_total_proteins_by_total_genomes = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)

    genomes = models.ManyToManyField(
        "GenomeMetadata",
        through="TaxonGenomeLink",
        related_name="mist_taxon_statistics"
    )

    class Meta:
        unique_together = ('gtdb_taxonomy_string', 'protein_type', 'domains')


class TaxonGenomeLink(models.Model):
    taxon = models.ForeignKey(DomainStatisticsPerTaxon, on_delete=models.CASCADE)
    genome = models.ForeignKey(GenomeMetadata, on_delete=models.CASCADE)