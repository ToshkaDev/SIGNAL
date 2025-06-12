import factory
from signalp.models import GenomeMetadata, DomainStatisticsPerProtein, DomainStatisticsPerGenome, DomainStatisticsPerTaxon
from signalp.models import ProteinType, Source, DomainCombinationType

class GenomeMetadataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenomeMetadata

    genome_version="GCF_000009965.1"
    genome_accession = "GCF_000009965"
    genome_size = 2088737
    protein_count = 2314
    # GTDB taxonomy
    gtdb_kingdom = "Archaea"
    gtdb_phylum = "Methanobacteriota_B"
    gtdb_class = "Thermococci"
    gtdb_order = "Thermococcales"
    gtdb_family = "Thermococcaceae"
    gtdb_genus = "Thermococcus"
    gtdb_species = "Thermococcus kodakarensis"
    # NCBI taxonomy
    ncbi_kingdom = "Archaea"
    ncbi_phylum = "Euryarchaeota"
    ncbi_class = "Thermococci"
    ncbi_order = "Thermococcales"
    ncbi_family = "Thermococcaceae"
    ncbi_genus = "Thermococcus"
    ncbi_species = "Thermococcus kodakarensis"

class DomainStatisticsPerProteinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DomainStatisticsPerProtein

    genome = factory.SubFactory(GenomeMetadataFactory)
    genome_accession="GCF_000009965"
    ncbi_protein_accession="WP_011249583.1"
    mist_protein_accession="GCF_000009965.1-TK_RS031251"
    protein_type=ProteinType.RR
    source=Source.MIST
    protein_length=120
    domain_architecture="Response_reg:4-115"
    sensors_or_regulators="nodomain"
    domain_counts={"Response_reg":1}
    domains="Response_reg"

class DomainStatisticsPerGenomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DomainStatisticsPerGenome

    genome = factory.SubFactory(GenomeMetadataFactory)
    genome_accession = "GCF_000009965"
    source = Source.MIST
    protein_type = ProteinType.HK
    domains = "PAS_3,PAS_4,PAS_9"
    domain_combination_type = DomainCombinationType.domain_comb
    count_raw = 2
    count_normalized_by_genome_size = 4.882401262588967e-07
    count_normalized_by_total_proteins = 0.0005752085130859936

class DomainStatisticsPerTaxonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DomainStatisticsPerTaxon

    gtdb_taxonomy_string = "Archaea;Halobacteriota;Methanomicrobia;Methanomicrobiales"
    gtdb_taxonomy_last = "Methanomicrobiales"
    gtdb_taxonomy_rank = "order"
    source =  Source.MIST
    protein_type = ProteinType.HK
    domains = "PAS_Fold,PAS_Fold,Peripla_BP"
    domain_combination_type = "superfamily_comb"
    count_raw = 2
    count_normalized_by_total_genomes = 0.044444444444444446
    count_normalized_by_genome_size_by_total_genomes = 1.3871828395608659e-08
    count_normalized_by_total_proteins_by_total_genomes = 1.4503720851844221e-05