from django.urls import path
from signalp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('genomes/', views.GenomeMetadataList.as_view(), name='genome_metadata-list'),
    path('genomes/<int:pk>/', views.GenomeMetadataDetail.as_view(), name='genome_metadata-detail'),
    path('protein-stats/', views.DomainStatisticsPerProteinList.as_view(), name='domain_statistics_perprotein-list'),
    path('protein-stats/<int:pk>/', views.DomainStatisticsPerProteinDetail.as_view(), name='domain_statistics_perprotein-detail'),
    path('genome-stats/', views.DomainStatisticsPerGenomeList.as_view(), name='domain_statistics_pergenome-list'),
    path('genome-stats/<int:pk>/', views.DomainStatisticsPerGenomeDetail.as_view(), name='domain_statistics_pergenome-detail'),
    path('taxon-stats/', views.DomainStatisticsPerTaxonList.as_view(), name='domain_statistics_pertaxon-list'),
    path('taxon-stats/<int:pk>/', views.DomainStatisticsPerTaxonDetail.as_view(), name='domain_statistics_pertaxon-detail'),
])

