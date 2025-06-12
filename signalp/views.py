from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from signalp.models import GenomeMetadata, DomainStatisticsPerProtein, DomainStatisticsPerGenome, DomainStatisticsPerTaxon
from signalp.serializers import GenomeMetadataSerializer, DomainStatisticsPerProteinSerializer, DomainStatisticsPerGenomeSerializer, DomainStatisticsPerTaxonSerializer
from signalp.custom_filters import DomainStatisticsPerProteinFilter, DomainStatisticsPerGenomeFilter, DomainStatisticsPerTaxonFilter


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'genomes': reverse('genome_metadata-list', request=request, format=format),
        'protein-stats': reverse('domain_statistics_perprotein-list', request=request, format=format),
        'genome-stats': reverse('domain_statistics_pergenome-list', request=request, format=format),
        'taxon-stats': reverse('domain_statistics_pertaxon-list', request=request, format=format),
    })


class GenomeMetadataList(generics.ListAPIView):
    queryset = GenomeMetadata.objects.all()
    serializer_class = GenomeMetadataSerializer
    filterset_fields = ['genome_version', 'genome_accession', 'genome_size', 'protein_count']
    search_fields = ['gtdb_kingdom', 'gtdb_phylum', 'gtdb_class', 'gtdb_order', 'gtdb_family', 'gtdb_genus', 'gtdb_species', 'ncbi_kingdom', 'ncbi_phylum',
                     'ncbi_class', 'ncbi_order', 'ncbi_family', 'ncbi_genus', 'ncbi_species']

class GenomeMetadataDetail(generics.RetrieveAPIView):
    queryset = GenomeMetadata.objects.all()
    serializer_class = GenomeMetadataSerializer


class DomainStatisticsPerProteinList(generics.ListAPIView):
    queryset = DomainStatisticsPerProtein.objects.all()
    serializer_class = DomainStatisticsPerProteinSerializer
    filterset_class = DomainStatisticsPerProteinFilter
    search_fields = ['domains', 'domain_architecture', 'sensors_or_regulators']

class DomainStatisticsPerProteinDetail(generics.RetrieveAPIView):
    queryset = DomainStatisticsPerProtein.objects.all()
    serializer_class = DomainStatisticsPerProteinSerializer


class DomainStatisticsPerGenomeList(generics.ListAPIView):
    queryset = DomainStatisticsPerGenome.objects.all()
    serializer_class = DomainStatisticsPerGenomeSerializer
    filterset_class = DomainStatisticsPerGenomeFilter
    search_fields = ['domains']

class DomainStatisticsPerGenomeDetail(generics.RetrieveAPIView):
    queryset = DomainStatisticsPerGenome.objects.all()
    serializer_class = DomainStatisticsPerGenomeSerializer


class DomainStatisticsPerTaxonList(generics.ListAPIView):
    queryset = DomainStatisticsPerTaxon.objects.all()
    serializer_class = DomainStatisticsPerTaxonSerializer
    filterset_class = DomainStatisticsPerTaxonFilter
    filterset_fields = ['gtdb_taxonomy_last', 'genome_accession', 'source', 'protein_type']
    search_fields = ['gtdb_taxonomy_last', 'domains']

class DomainStatisticsPerTaxonDetail(generics.RetrieveAPIView):
    queryset = DomainStatisticsPerTaxon.objects.all()
    serializer_class = DomainStatisticsPerTaxonSerializer

