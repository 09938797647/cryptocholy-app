build:
	docker compose build

compile-translations:
	./scripts/compile-translations.sh

down:
	docker compose down

restart: stop run

run:
	docker compose up -d

setup:
	./scripts/setup.sh

stop:
	docker compose stop
