.PHONY: build-prod up-prod down-prod build-dev up-dev down-dev logs

# Production commands
build-prod:
	docker-compose -f docker-compose.prod.yml build

up-prod:
	docker-compose -f docker-compose.prod.yml up -d

down-prod:
	docker-compose -f docker-compose.prod.yml down

logs:
	docker-compose -f docker-compose.prod.yml logs -f

# Development commands
build-dev:
	docker-compose -f docker-compose.dev.yml build

up-dev:
	docker-compose -f docker-compose.dev.yml up -d

down-dev:
	docker-compose -f docker-compose.dev.yml down

make_migrations-dev:
	docker-compose -f docker-compose.dev.yml exec django python manage.py makemigrations signalp

migrate-dev:
	docker-compose -f docker-compose.dev.yml exec django python manage.py migrate

load_genome_metadata-dev:
	docker-compose -f docker-compose.dev.yml exec django python manage.py load_genome_metadata

load_per_genome_stats-dev:
	docker-compose -f docker-compose.dev.yml exec django python manage.py load_per_genome_stats

load_per_protein_stats-dev:
	docker-compose -f docker-compose.dev.yml exec django python manage.py load_per_protein_stats

load_per_taxon_stats-dev:
	docker-compose -f docker-compose.dev.yml exec django python manage.py load_per_taxon_stats

load_data:
	make load_genome_metadata-dev load_per_genome_stats-dev load_per_protein_stats-dev load_per_taxon_stats-dev
		
# With optional --file param:
#load-dev:
#	docker-compose -f docker-compose.dev.yml exec django python manage.py load_genome_metadata.py --file path/to/file.tsv

# usage example: make build-dev
# make load_genome_metadata-dev load_per_genome_stats-dev load_per_protein_stats-dev load_per_taxon_stats-dev