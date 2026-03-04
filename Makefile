.PHONY: help build up down logs shell migrate makemigrations createsuperuser populate

help:
	@echo "Available commands:"
	@echo "  make build           - Build or rebuild services"
	@echo "  make up              - Create and start containers"
	@echo "  make down            - Stop and remove containers, networks"
	@echo "  make logs            - View output from containers"
	@echo "  make shell           - Access the Django shell"
	@echo "  make migrate         - Run database migrations"
	@echo "  make makemigrations  - Create new database migrations"
	@echo "  make createsuperuser - Create a Django superuser"
	@echo "  make populate        - Run populate.py to seed the database with fake data"

build:
	docker-compose build

up:
	python3 verify-templates.py --fix
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

populate:
	docker-compose exec web python populate.py
