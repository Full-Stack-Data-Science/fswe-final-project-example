.PHONY:
.ONESHELL:

include .env
export

infra-up:
	docker compose -f ./docker-compose.yml up -d

infra-logs:
	docker compose -f ./docker-compose.yml logs
	
infra-down:
	docker compose -f ./docker-compose.yml down -v
