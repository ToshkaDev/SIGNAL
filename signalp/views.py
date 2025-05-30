from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from signalp.models import GenomeMetadata, DomainStatisticsPerProtein, DomainStatisticsPerGenome, DomainStatisticsPerTaxon
from signalp.serializers import GenomeMetadataSerializer, DomainStatisticsPerProteinSerializer, DomainStatisticsPerGenomeSerializer, DomainStatisticsPerTaxonSerializer


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

class GenomeMetadataDetail(generics.RetrieveAPIView):
    queryset = GenomeMetadata.objects.all()
    serializer_class = GenomeMetadataSerializer


class DomainStatisticsPerProteinList(generics.ListAPIView):
    queryset = DomainStatisticsPerProtein.objects.all()
    serializer_class = DomainStatisticsPerProteinSerializer

class DomainStatisticsPerProteinDetail(generics.RetrieveAPIView):
    queryset = DomainStatisticsPerProtein.objects.all()
    serializer_class = DomainStatisticsPerProteinSerializer


class DomainStatisticsPerGenomeList(generics.ListAPIView):
    queryset = DomainStatisticsPerGenome.objects.all()
    serializer_class = DomainStatisticsPerGenomeSerializer

class DomainStatisticsPerGenomeDetail(generics.RetrieveAPIView):
    queryset = DomainStatisticsPerGenome.objects.all()
    serializer_class = DomainStatisticsPerGenomeSerializer


class DomainStatisticsPerTaxonList(generics.ListAPIView):
    queryset = DomainStatisticsPerTaxon.objects.all()
    serializer_class = DomainStatisticsPerTaxonSerializer

class DomainStatisticsPerTaxonDetail(generics.RetrieveAPIView):
    queryset = DomainStatisticsPerTaxon.objects.all()
    serializer_class = DomainStatisticsPerTaxonSerializer