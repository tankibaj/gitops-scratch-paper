# HashiCorp Vault

HashiCorp Vault is a secrets management tools that provides a secure, centralized way to store, access, and manage sensitive information like API keys, passwords, tokens, and encryption keys. Vault is designed to help organizations minimize the risk of data breaches and simplify the process of managing secrets across distributed systems and applications.

## Prepare Storage Backend

You can either choose `HashiCorp Consul` or `PostgreSQL` as a [storage backend for HashiCorp Vault](https://developer.hashicorp.com/vault/docs/configuration/storage).
- [Consul Storage Backend](consul.md)
- [PostgreSQL Storage Backend](prepare-database/vault-postgres-storage-backend)

## Initialize Vault

- Initialize `vault-0` with one key share and one key threshold
  ```bash
  kubectl -n vault exec vault-0 -- vault operator init \
      -key-shares=1 \
      -key-threshold=1 \
      -format=json > vault-keys.json
  ```
  > NOTE: A single key share and a single key threshold are not recommended in Vault production.

- Create a variable of vault unseal key
  ```bash
  VAULT_UNSEAL_KEY=$(jq -r ".unseal_keys_b64[]" vault-keys.json)
  ```
  
- Unseal Vault
  ```bash
  kubectl -n vault exec vault-0 -- vault operator unseal $VAULT_UNSEAL_KEY
  kubectl -n vault exec vault-1 -- vault operator unseal $VAULT_UNSEAL_KEY
  kubectl -n vault exec vault-2 -- vault operator unseal $VAULT_UNSEAL_KEY
  ```

<br/>

## Vault CLI Authentication

- Install Vault

  ```bash
  brew install vault
  ```

- Set a variable of vault url

    ```bash
    export VAULT_ADDR=https://$(kubectl get ingress -n vault -o=jsonpath='{.items[0].spec.rules[0].host}')
    ```

- Set a variable of vault root token

    ```bash
   export VAULT_TOKEN=$(cat vault-keys.json | jq -r ".root_token")
    ```

- Check vault cluster status

    ```bash
    vault status
    ```
  
## Vault Configuration (optional)

### Secret Engine

- Enable a `KV secrets engine` version2 at the path `secrets/`. The `kv` secrets engine is used to store arbitrary secrets within the configured physical storage for Vault.
  ```bash
  vault secrets enable -path=secrets -version=2 kv
  ```
- Verify secrets engine
  ```bash
  vault secrets list
  ```

### Secrets
- List secrets
  ```bash
  vault kv list secret
  ```
- Set a secret name variable
   ```bash
   VAUL_SECRET_NAME=mySecret
   ```
- Create or update secret
   ```bash
   vault kv put -mount=secrets ${VAUL_SECRET_NAME} username=foo password=bar
   ```
- Fetch secret
  ```bash
  vault kv get secret/${VAUL_SECRET_NAME}
  ```