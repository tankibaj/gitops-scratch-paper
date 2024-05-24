## Preparing the Database for Keycloak

### Step 1: Connect to PostgreSQL as a Superuser

1. **Connect to PostgreSQL as a Superuser**

   First, connect to your PostgreSQL instance as a superuser (usually `postgres`):

   ```sh
   export POSTGRES_HOST=postgres.postgres
   export POSTGRES_USER=postgres
   export POSTGRES_DB=postgres
   export POSTGRES_PASSWORD=$(kubectl get secret --namespace postgres postgres-secret -o jsonpath="{.data.adminPassword}" | base64 --decode)
   ```
    
   ```sh
   kubectl run postgres-client --rm --tty -i \
        --image bitnami/postgresql \
        --env="PGPASSWORD=$POSTGRES_PASSWORD" \
        -- psql --host $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB
   ```

### Step 2: Create the Database and User

1. **Create the Role and User**

   Create a role (`keycloak_dba`) and a user with the necessary permissions:

   ```sql
   -- Create the role keycloak_dba
   CREATE ROLE keycloak_dba;

   -- Create the user keycloak with the keycloak_dba role and specified password
   CREATE USER keycloak WITH ENCRYPTED PASSWORD '9uwiPiMMAEQ8';
   ALTER USER keycloak WITH LOGIN;
   GRANT keycloak_dba TO keycloak;
   ```

2. **Create the Database and Grant Permissions**

   Create the `keycloak` database and grant the necessary permissions to the `keycloak_dba` role:

   ```sql
   -- Create the keycloak database
   CREATE DATABASE keycloak;

   -- Connect to the keycloak database
   \c keycloak

   -- Grant permissions to keycloak_dba on the keycloak database
   GRANT CONNECT ON DATABASE keycloak TO keycloak_dba;
   GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak_dba;

   -- Grant all privileges on the public schema to the keycloak_dba role
   GRANT ALL ON SCHEMA public TO keycloak_dba WITH GRANT OPTION;

   -- Grant all privileges on all tables, sequences, and functions in the public schema to the keycloak_dba role
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO keycloak_dba;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO keycloak_dba;
   GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO keycloak_dba;

   -- Ensure the keycloak_dba role has default privileges for future objects
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO keycloak_dba;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO keycloak_dba;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO keycloak_dba;
   ```

### Step 3: Verify

1. To verify that the permissions are set correctly, you can list the permissions for the `keycloak_dba` role and `keycloak` user on the `keycloak` database:

    ```sql
        -- List the privileges on the keycloak database
        \l+ keycloak
        
        -- List the privileges on the public schema
        \dn+
    ```

2. To verify that the `keycloak` user can connect to the `keycloak` database, you can connect to the database as the `keycloak` user:

    ```sh
    export POSTGRES_USER=keycloak
    export POSTGRES_DB=keycloak
    export POSTGRES_PASSWORD=9uwiPiMMAEQ8
    ```

    ```sh
    kubectl run postgres-client --rm --tty -i \
        --image bitnami/postgresql \
        --env="PGPASSWORD=$POSTGRES_PASSWORD" \
        -- psql --host $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB
    ```