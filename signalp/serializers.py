from rest_framework import serializers
from signalp.models import GenomeMetadata, DomainStatisticsPerProtein, DomainStatisticsPerGenome, DomainStatisticsPerTaxon

class GenomeMetadataSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='genome_metadata-detail')
    domain_statistics_perprotein = serializers.HyperlinkedRelatedField(many=True, view_name='domain_statistics_perprotein-detail', read_only=True)
    domain_statistics_pergenome = serializers.HyperlinkedRelatedField(many=True, view_name='domain_statistics_pergenome-detail', read_only=True)
    # We do not expose related items as each genome is associated with an exessive number of related DomainStatisticsPerTaxon entries
    # domain_statistics_pertaxon = serializers.HyperlinkedRelatedField(many=True, view_name='domain_statistics_pertaxon-detail', source='mist_taxon_statistics', read_only=True)

    class Meta:
        model = GenomeMetadata
        fields = ['url', 'id', 'genome_version', 'genome_accession', 'genome_size', 'protein_count', 
                  'gtdb_kingdom', 'gtdb_phylum', 'gtdb_class', 'gtdb_order', 'gtdb_family', 'gtdb_genus', 'gtdb_species',
                  'ncbi_kingdom', 'ncbi_phylum', 'ncbi_class', 'ncbi_order', 'ncbi_family', 'ncbi_genus', 'ncbi_species',
                  'domain_statistics_perprotein', 'domain_statistics_pergenome']
        
class DomainStatisticsPerProteinSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='domain_statistics_perprotein-detail')

    class Meta:
        model = DomainStatisticsPerProtein
        fields = ['url', 'id', 'genome', 'genome_accession', 'ncbi_protein_accession', 'mist_protein_accession', 
                  'protein_type', 'source', 'protein_length', 'domain_architecture', 'sensors_or_regulators', 'domain_counts', 'domains']

class DomainStatisticsPerGenomeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='domain_statistics_pergenome-detail')

    class Meta:
        model = DomainStatisticsPerGenome
        fields = ['url', 'id', 'genome', 'genome_accession', 'source', 'protein_type', 'domains', 'domain_combination_type', 
                  'count_raw', 'count_normalized_by_genome_size', 'count_normalized_by_total_proteins']

class DomainStatisticsPerTaxonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='domain_statistics_pertaxon-detail')
    genomes = serializers.HyperlinkedRelatedField(many=True, view_name='genome_metadata-detail', read_only=True)

    class Meta:
        model = DomainStatisticsPerTaxon
        fields = ['url', 'id', 'gtdb_taxonomy_string', 'gtdb_taxonomy_last', 'gtdb_taxonomy_rank', 'source', 'protein_type', 'domains', 
                  'domain_combination_type', 'count_raw', 'count_normalized_by_total_genomes',
                  'count_normalized_by_genome_size_by_total_genomes', 'count_normalized_by_total_proteins_by_total_genomes', 'genomes']