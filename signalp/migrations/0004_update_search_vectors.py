from django.db import migrations, models
from django.contrib.postgres.search import SearchVector

def update_search_vector(apps, schema_editor):
    models_to_update = [
        ('signalp', 'DomainStatisticsPerProtein', 'domains'),
        ('signalp', 'DomainStatisticsPerGenome', 'domains'),
        ('signalp', 'DomainStatisticsPerTaxon', 'domains'),
    ]

    for app_label, model_name, source_field in models_to_update:
        Model = apps.get_model(app_label, model_name)
        Model.objects.update(
            search_vector=SearchVector(source_field)
        )

class Migration(migrations.Migration):

    dependencies = [
        ('signalp', '0003_remove_domainstatisticsperprotein_domain_combination_and_more'),
    ]
    
    operations = [
        # 1. First, run the initial update on existing rows
        migrations.RunPython(update_search_vector),

        # 2. Then add the PostgreSQL trigger for automatic future updates
        migrations.RunSQL(
            """
            -- Create a reusable trigger function
            CREATE FUNCTION update_search_vector() RETURNS trigger AS $$
            BEGIN
                NEW.search_vector := to_tsvector('english', NEW.domains);
                RETURN NEW;
            END
            $$ LANGUAGE plpgsql;

            -- Trigger for DomainStatisticsPerProtein
            CREATE TRIGGER domain_stats_protein_search_vector_trigger
            BEFORE INSERT OR UPDATE ON signalp_domainstatisticsperprotein
            FOR EACH ROW EXECUTE FUNCTION update_search_vector();

            -- Trigger for DomainStatisticsPerGenome
            CREATE TRIGGER domain_stats_genome_search_vector_trigger
            BEFORE INSERT OR UPDATE ON signalp_domainstatisticspergenome
            FOR EACH ROW EXECUTE FUNCTION update_search_vector();

            -- Trigger for DomainStatisticsPerTaxon
            CREATE TRIGGER domain_stats_taxon_search_vector_trigger
            BEFORE INSERT OR UPDATE ON signalp_domainstatisticspertaxon
            FOR EACH ROW EXECUTE FUNCTION update_search_vector();
            """,

            reverse_sql="""
            -- Drop all three triggers
            DROP TRIGGER IF EXISTS domain_stats_protein_search_vector_trigger ON signalp_domainstatisticsperprotein;
            DROP TRIGGER IF EXISTS domain_stats_genome_search_vector_trigger ON signalp_domainstatisticspergenome;
            DROP TRIGGER IF EXISTS domain_stats_taxon_search_vector_trigger ON signalp_domainstatisticspertaxon;

            -- Drop the trigger function (if not used elsewhere)
            DROP FUNCTION IF EXISTS update_search_vector();
            """
        ),
    ]