from django.test import TestCase
from signalp.models import DomainStatisticsPerProtein, GenomeMetadata, ProteinType, Source



class DomainStatisticsPerProteinModelTest(TestCase):
    genome_version="GCF_000009965.1"
    genome_accession = "GCF_000009965"

    def setUp(self):
        self.genome = self.createGenomeMetadataObject()
    
    def createGenomeMetadataObject(self):
        return GenomeMetadata.objects.create(
            genome_version=self.genome_version,
            genome_accession = self.genome_accession,
            genome_size = 2088737,
            protein_count = 2314,
            # GTDB taxonomy
            gtdb_kingdom = "Archaea",
            gtdb_phylum = "Methanobacteriota_B",
            gtdb_class = "Thermococci",
            gtdb_order = "Thermococcales",
            gtdb_family = "Thermococcaceae",
            gtdb_genus = "Thermococcus",
            gtdb_species = "Thermococcus kodakarensis",
            # NCBI taxonomy
            ncbi_kingdom = "Archaea",
            ncbi_phylum = "Euryarchaeota",
            ncbi_class = "Thermococci",
            ncbi_order = "Thermococcales",
            ncbi_family = "Thermococcaceae",
            ncbi_genus = "Thermococcus",
            ncbi_species = "Thermococcus kodakarensis"
        )   

    def createDomainStatisticsPerProteinObject(self, mist_protein_accession="GCF_000009965.1-TK_RS031251", 
                                               protein_type=ProteinType.RR, source=Source.MIST, 
                                               domain_architecture="Response_reg:4-115", domains="Response_reg"):
        return DomainStatisticsPerProtein.objects.create(
            genome=self.genome,
            genome_accession=self.genome_accession,
            ncbi_protein_accession="WP_011249583.1",
            mist_protein_accession=mist_protein_accession,
            protein_type=protein_type,
            source=source,
            protein_length=120,
            domain_architecture=domain_architecture,
            sensors_or_regulators="nodomain",
            domain_counts={"Response_reg":1},
            domains=domains
        )
    
    def test_create_valid_domain_statistics_per_protein(self):
        obj = self.createDomainStatisticsPerProteinObject(mist_protein_accession="GCF_000009965.1-TK_RS031251")
        self.assertEqual(obj.mist_protein_accession, "GCF_000009965.1-TK_RS031251")

    def test_unique_mist_protein_accession(self):
        self.createDomainStatisticsPerProteinObject()
        with self.assertRaises(Exception):
            self.createDomainStatisticsPerProteinObject()
            
    def test_null_optional_fields(self):
        obj = self.createDomainStatisticsPerProteinObject(domain_architecture=None, domains=None)
        self.assertIsNone(obj.domain_architecture)
        self.assertIsNone(obj.search_vector)

    def test_genome_foreign_key(self):
        obj = self.createDomainStatisticsPerProteinObject()
        self.assertEqual(obj.genome.genome_version, self.genome_version)

    def test_search_vector_index_exists(self):
        index_names = [index.name for index in DomainStatisticsPerProtein._meta.indexes]
        self.assertIn("search_vector_prot_idx", index_names)