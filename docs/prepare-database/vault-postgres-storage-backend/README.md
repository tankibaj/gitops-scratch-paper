# PostgreSQL Storage Backend for Vault HA Cluster

This directory contains the necessary scripts and SQL files to set up a Vault storage backend using PostgreSQL.

## Prerequisites

- `kubectl` command line tool installed and configured to connect to your Kubernetes cluster

## Environment Variables
Before running the script, you need to set the following environment variables:

- `POSTGRES_ENDPOINT`: The endpoint of your RDS PostgreSQL instance
- `POSTGRES_USERNAME`: The username for connecting to the RDS instance
- `POSTGRES_PASSWORD`: The password for the PostgreSQL user
- `POSTGRES_DATABASE`: The initial database to connect to (usually "postgres")
- `VAULT_USER_PASSWORD`: The password for the "vault" user that will be created

You can set these environment variables in your terminal session like this:

```bash
export POSTGRES_ENDPOINT="<RDS_ENDPOINT>"
export POSTGRES_USERNAME="<RDS_USERNAME>"
export POSTGRES_PASSWORD="<RDS_PASSWORD>"
export POSTGRES_DATABASE="<RDS_DATABASE>"
export VAULT_USER_PASSWORD="<VAULT_USER_PASSWORD>"
```

## Files

- `vault-db-init`: Bash script to create a PostgreSQL client pod in the EKS cluster, execute the SQL commands, and set up the Vault storage backend
- `init.sql`: SQL commands to create the "vault" user and the "vault_db" database
- `table.sql`: SQL commands to create the necessary tables and grant the required permissions for the Vault storage backend

## Usage

- Set the environment variables as described in the [Environment Variables](#Environment-Variables) section.
- Run the `vault-db-init` script:

    ```bash
    ./vault-db-init
    ```
- Once the script completes successfully, your PostgreSQL instance is ready to be used as a Vault storage backend. You can now configure your Vault instance to use the PostgreSQL instance.