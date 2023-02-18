## Overview

[Harbor](https://goharbor.io) is an open source container image registry that secures artifacts with policies and role-based access control, ensures images are scanned and free from vulnerabilities, and signs images as trusted.

#### Prepare database

Create a postgres client pod on the Kubernetes cluster to login into the database.

```bash
export POSTGRES_HOST=postgres.local.naim.run
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=<passowrd>

kubectl run postgres-client --rm --tty -i \
	--image bitnami/postgresql \
	--env="PGPASSWORD=$POSTGRES_PASSWORD" \
	--command -- psql --host $POSTGRES_HOST -U $POSTGRES_USER

```

Create a postgres user with login privilege

```bash
CREATE ROLE harbor;
ALTER USER harbor ENCRYPTED PASSWORD '<password>'; # See path: harbor/secrets.enc.yaml
ALTER ROLE harbor with LOGIN;
```

List all user accounts (or roles)

```bash
\du
```

Create `registry` database and grant login privilege to `harbor` user

```bash
CREATE DATABASE registry;
\c registry
GRANT CONNECT ON DATABASE registry to harbor;
GRANT ALL ON SCHEMA public TO harbor WITH GRANT OPTION;
```

List all databases

```
\l
```

#### Secrets encryption using `sops`

```bash
sops -e harbor/secrets.default.yaml > harbor/secrets.enc.yaml
```

#### Harbor Installation

```bash
kubectl apply -f ../applications/harbor.yaml
```

