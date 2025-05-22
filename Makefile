DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
BASE_ENV = --env-file env/.env.default
ENV = --env-file env/.env.docker

ALL_FILE = docker_compose/all.yml
ALL_WK_FILE = docker_compose/all-wk.yml
APP_FILE = docker_compose/app.yml
DB_FILE = docker_compose/db.yml
KAFKA_FILE = docker_compose/kafka.yml
REDIS_FILE = docker_compose/redis.yml

APP_CONTAINER = monolith-backend-boilerplate-app
DB_CONTAINER = monolith-backend-boilerplate-db
KAFKA_CONTAINER = monolith-backend-boilerplate-kafka
REDIS_CONTAINER = monolith-backend-boilerplate-redis

.PHONY: ruff
ruff:
	ruff format && ruff check --fix

.PHONY: alembic
alembic:
	alembic revision --autogenerate -m "$(m)"

.PHONY: all
all:
	$(DC) -f $(ALL_FILE) -f $(DB_FILE) -f $(KAFKA_FILE) -f $(REDIS_FILE) $(BASE_ENV) $(ENV) up --build -d  --force-recreate

.PHONY: all-down
all-down:
	$(DC) -f $(ALL_FILE) -f $(DB_FILE) -f $(KAFKA_FILE) $(BASE_ENV) -f $(REDIS_FILE) $(ENV) down

.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(BASE_ENV) $(ENV) up --build -d  --force-recreate

.PHONY: app-shell
app-shell:
	$(EXEC) $(APP_CONTAINER) bash

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) $(BASE_ENV) $(ENV) down

.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f

.PHONY: db
db:
	$(DC) -f $(DB_FILE) $(BASE_ENV) $(ENV) up --build -d

.PHONY: db-shell
db-shell:
	$(EXEC) $(DB_CONTAINER) bash

.PHONY: db-down
db-down:
	$(DC) -f $(DB_FILE) $(BASE_ENV) $(ENV) down

.PHONY: db-logs
db-logs:
	$(LOGS) $(DB_CONTAINER) -f

.PHONY: kafka
kafka:
	$(DC) -f $(KAFKA_FILE) $(BASE_ENV) $(ENV) up --build -d

.PHONY: kafka-shell
kafka-shell:
	$(EXEC) $(KAFKA_CONTAINER) bash

.PHONY: kafka-down
kafka-down:
	$(DC) -f $(KAFKA_FILE) $(BASE_ENV) $(ENV) down

.PHONY: kafka-logs
kafka-logs:
	$(LOGS) $(KAFKA_CONTAINER) -f

.PHONY: redis
redis:
	$(DC) -f $(REDIS_FILE) $(BASE_ENV) $(ENV) up --build -d

.PHONY: redis-shell
redis-shell:
	$(EXEC) $(REDIS_CONTAINER) bash

.PHONY: redis-down
redis-down:
	$(DC) -f $(REDIS_FILE) $(BASE_ENV) $(ENV) down

.PHONY: redis-logs
redis-logs:
	$(LOGS) $(REDIS_CONTAINER) -f
