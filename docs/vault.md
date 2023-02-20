# Vault by HashiCorp
Vault secures, stores, and tightly controls access to tokens, passwords, certificates, API keys, and other secrets in modern computing.

```bash
kubectl apply -f ../applications/vault.yaml
```

<br/>

## Initialize Vault

### Display all the pods within the `vault` namespace

```bash
kubectl -n vault get pods
```

### Initialize vault-0 with one key share and one key threshold.

```bash
kubectl -n vault exec vault-0 -- vault operator init \
    -key-shares=1 \
    -key-threshold=1 \
    -format=json > vault-keys.json
```

The [`operator init`](https://developer.hashicorp.com/vault/docs/commands/operator/init) command generates a root key that it disassembles into key shares `-key-shares=1` and then sets the number of key shares required to unseal Vault `-key-threshold=1`. These key shares are written to the output as unseal keys in JSON format `-format=json`. Here the output is redirected to a file named `cluster-keys.json`.

### Display the unseal key found in `vault-keys.json`.

```bash
jq -r ".unseal_keys_b64[]" vault-keys.json
```

**Insecure operation:** Do not run an unsealed Vault in production with a single key share and a single key threshold. This approach is only used here to simplify the unsealing process for this demonstration.

### Create a variable named `VAULT_UNSEAL_KEY` to capture the Vault unseal key.

```bash
VAULT_UNSEAL_KEY=$(jq -r ".unseal_keys_b64[]" vault-keys.json)
```

After initialization, Vault is configured to know where and how to access the storage, but does not know how to decrypt any of it. [Unsealing](https://developer.hashicorp.com/vault/docs/concepts/seal#unsealing) is the process of constructing the root key necessary to read the decryption key to decrypt the data, allowing access to the Vault.

### Unseal Vault running on the `vault-0` pod.

```bash
kubectl -n vault exec vault-0 -- vault operator unseal $VAULT_UNSEAL_KEY
```

**Insecure operation:** Providing the unseal key with the command writes the key to your shell's history. This approach is only used here to simplify the unsealing process for this demonstration.

The `operator unseal` command reports that Vault is initialized and unsealed.

**Example output:**

```text
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.12.1
Build Date      2022-10-27T12:32:05Z
Storage Type    consul
Cluster Name    vault-cluster-d6d53090
Cluster ID      4b8727be-c2f0-2400-c92e-d2a730cfaec7
HA Enabled      true
HA Cluster      https://vault-0.vault-internal:8201
HA Mode         active
Active Since    2023-02-19T05:40:07.135944348Z
```

The Vault server is initialized and unsealed.

### Unseal Vault running on the `vault-1` pod.

```bash
kubectl -n vault exec vault-1 -- vault operator unseal $VAULT_UNSEAL_KEY
```

### Unseal Vault running on the `vault-2` pod.

```bash
kubectl -n vault exec vault-2 -- vault operator unseal $VAULT_UNSEAL_KEY
```

Verify all the Vault pods are running and ready.

```bash
kubectl -n vault get pods
```

Example output:

```text
NAME                                    READY   STATUS    RESTARTS   AGE
vault-0                                 1/1     Running   0          5m49s
vault-1                                 1/1     Running   0          5m48s
vault-2                                 1/1     Running   0          5m47s
vault-agent-injector-5945fb98b5-vzbqv   1/1     Running   0          5m50s
```

<br/>

## Vault CLI client

Create a variable named `VAULT_ROOT_KEY` and `VAULT_ADDR` to capture the Vault root token and endpoint.

```bash
VAULT_ROOT_KEY=$(cat vault-keys.json | jq -r ".root_token")
```

```bash
export VAULT_ADDR=https://vault.local.naim.run
```

Vault is now ready for you. Lets check vault status:

```bash
vault status
```



## Secrets Engines

Secrets engines are Vault components which store, generate or encrypt secrets.

### Enable a secrets engine

To get started, enable a new KV secrets engine at the path `secret`. Each path is completely isolated and cannot talk to other paths. For example, a KV secrets engine enabled at `foo` has no ability to communicate with a KV secrets engine enabled at `bar`.

```bash
vault secrets enable -path=secret kv-v2
```

To verify our success and get more information about the secrets engine, use the `vault secrets list` command:

```bash
vault secrets list
```

**Output**

```text
Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_245571c4    per-token private secret storage
identity/     identity     identity_6c094184     identity store
kv/           kv           kv_e5b3a51e           n/a
secret/       kv           kv_9b6a980c           n/a
sys/          system       system_f45198e2       system endpoints used for control, policy and debugging
```

### Create a secret

Create a secret at path `secret/webapp/config` with a `username` and `password`.

```bash
vault kv put secret/webapp/config username="static-user" password="static-password"
```

**Output**

```text
====== Secret Path ======
secret/data/webapp/config

======= Metadata =======
Key                Value
---                -----
created_time       2023-02-20T23:14:58.455587859Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1
```

Verify that the secret is defined at the path `secret/webapp/config`.

```bash
vault kv get secret/webapp/config
```

**Output**

```text
====== Secret Path ======
secret/data/webapp/config

======= Metadata =======
Key                Value
---                -----
created_time       2023-02-20T23:14:58.455587859Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1

====== Data ======
Key         Value
---         -----
password    static-password
username    static-user
```



<br/>


## Next steps

You launched Vault in high-availability mode. Learn more about the Vault Helm chart by reading the documentations:

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-amazon-eks

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-google-cloud-gke

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-azure-aks

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-minikube-raft

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-minikube-consul

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-minikube-tls

https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-secrets-engines

Then you deployed a web application that authenticated and requested a secret directly from Vault. Explore how pods can retrieve secrets through the [Vault Injector service via annotations](https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-sidecar)or secrets [mounted on ephemeral volumes](https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-secret-store-driver).

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-external-vault
