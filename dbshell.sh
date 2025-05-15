#!/bin/sh
. ./.env.dev
docker exec -it $(docker ps -qf "name=postgres") psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"