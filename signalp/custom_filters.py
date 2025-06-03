import django_filters
from signalp.models import DomainStatisticsPerProtein, DomainStatisticsPerGenome, DomainStatisticsPerTaxon


class DomainStatisticsPerProteinFilter(django_filters.FilterSet):
    protein_length__gte = django_filters.NumberFilter(field_name='protein_length', lookup_expr='gte')
    protein_length__lte = django_filters.NumberFilter(field_name='protein_length', lookup_expr='lte')

    class Meta:
        model = DomainStatisticsPerProtein
        fields = ['protein_length__gte', 'protein_length__lte']

class DomainStatisticsPerGenomeFilter(django_filters.FilterSet):
    count_raw__gte = django_filters.NumberFilter(field_name='count_raw', lookup_expr='gte')
    count_raw__lte = django_filters.NumberFilter(field_name='count_raw', lookup_expr='lte')
    count_normalized_by_genome_size__gte = django_filters.NumberFilter(field_name='count_normalized_by_genome_size', lookup_expr='gte')
    count_normalized_by_genome_size__lte = django_filters.NumberFilter(field_name='count_normalized_by_genome_size', lookup_expr='lte')
    count_normalized_by_total_proteins__gte = django_filters.NumberFilter(field_name='count_normalized_by_total_proteins', lookup_expr='gte')
    count_normalized_by_total_proteins__lte = django_filters.NumberFilter(field_name='count_normalized_by_total_proteins', lookup_expr='lte')

    class Meta:
        model = DomainStatisticsPerGenome
        fields = ['count_raw__gte', 'count_raw__lte', 'count_normalized_by_genome_size__gte', 'count_normalized_by_genome_size__lte', 'count_normalized_by_total_proteins__gte', 'count_normalized_by_total_proteins__lte']


class DomainStatisticsPerTaxonFilter(django_filters.FilterSet):
    count_raw__gte = django_filters.NumberFilter(field_name='count_raw', lookup_expr='gte')
    count_raw__lte = django_filters.NumberFilter(field_name='count_raw', lookup_expr='lte')
    count_normalized_by_total_genomes__gte = django_filters.NumberFilter(field_name='count_normalized_by_total_genomes', lookup_expr='gte')
    count_normalized_by_total_genomes__lte = django_filters.NumberFilter(field_name='count_normalized_by_total_genomes', lookup_expr='lte')
    count_normalized_by_genome_size_by_total_genomes__gte = django_filters.NumberFilter(field_name='count_normalized_by_genome_size_by_total_genomes', lookup_expr='gte')
    count_normalized_by_genome_size_by_total_genomes__lte = django_filters.NumberFilter(field_name='count_normalized_by_genome_size_by_total_genomes', lookup_expr='lte')
    count_normalized_by_total_proteins_by_total_genomes__gte = django_filters.NumberFilter(field_name='count_normalized_by_total_proteins_by_total_genomes', lookup_expr='gte')
    count_normalized_by_total_proteins_by_total_genomes__lte = django_filters.NumberFilter(field_name='count_normalized_by_total_proteins_by_total_genomes', lookup_expr='lte')

    class Meta:
        model = DomainStatisticsPerTaxon
        fields = ['count_raw__gte', 'count_raw__lte', 'count_normalized_by_total_genomes__gte', 'count_normalized_by_total_genomes__lte', 
                  'count_normalized_by_genome_size_by_total_genomes__gte', 'count_normalized_by_genome_size_by_total_genomes__lte',
                  'count_normalized_by_total_proteins_by_total_genomes__gte', 'count_normalized_by_total_proteins_by_total_genomes__lte']
