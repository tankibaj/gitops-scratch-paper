## Overview
PostgreSQL (Postgres) is an open source object-relational database known for reliability and data integrity. ACID-compliant, it supports foreign keys, joins, views, triggers and stored procedures.

## Installation

```bash
kubectl apply -f ../applications/postgres.yaml
```

## Connecting to the Database

### Admin user access

```bash
export POSTGRES_HOST=postgres.postgres
export POSTGRES_USER=postgres
export POSTGRES_DB=postgres
export POSTGRES_PASSWORD=$(kubectl get secret --namespace postgres postgres-secret -o jsonpath="{.data.adminPassword}" | base64 --decode)
```


### Standard user access
```bash
export POSTGRES_HOST=postgres.postgres
export POSTGRES_USER=demouser
export POSTGRES_DB=demodb
export POSTGRES_PASSWORD=$(kubectl get secret --namespace postgres postgres-secret -o jsonpath="{.data.userPassword}" | base64 --decode)
```

### Spin up a client pod to connect to the database
```bash
kubectl run postgres-client --rm --tty -i \
	--image bitnami/postgresql \
	--env="PGPASSWORD=$POSTGRES_PASSWORD" \
	-- psql --host $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB
```

## Create a new database and user (optional)
```bash
export NEW_DB_NAME="keycloak19"
export NEW_USER="keycloak19"
export NEW_USER_PASSWORD="demo"
```

```bash
kubectl run postgres-client --rm --tty -i \
    --image bitnami/postgresql \
    --env="PGPASSWORD=$POSTGRES_PASSWORD" \
    -- bash -c "psql --host $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB <<-EOF
        \set AUTOCOMMIT off
        CREATE DATABASE IF NOT EXISTS $NEW_DB_NAME;
        CREATE USER IF NOT EXISTS $NEW_USER WITH PASSWORD '$NEW_USER_PASSWORD';
        GRANT ALL PRIVILEGES ON DATABASE $NEW_DB_NAME TO $NEW_USER;
        COMMIT;
EOF"
```

Cleanup
```bash
kubectl run postgres-client --rm --tty -i \
    --image bitnami/postgresql \
    --env="PGPASSWORD=$POSTGRES_PASSWORD" \
    -- bash -c "psql --host $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB <<-EOF
        \set AUTOCOMMIT off
        DROP DATABASE $NEW_DB_NAME;
        DROP USER $NEW_USER;
        COMMIT;
EOF"
```
