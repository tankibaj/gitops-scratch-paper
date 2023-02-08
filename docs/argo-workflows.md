## Overview
[Argo Workflows](https://argoproj.github.io/argo-workflows/) is an open source container-native workflow engine for orchestrating parallel jobs on Kubernetes.


## Prerequisite
Create the Kubernetes secrets for holding the OIDC `client-id` and `client-secret`.

```bash
kubectl -n argo create secret generic argo-server-sso \
  --from-literal=client-id=myclientid \
  --from-literal=client-secret=myclientsecret
```

Verify secrets

```bash
kubectl -n argo get secrets argo-server-sso -o jsonpath="{.data.client-id}" | base64 -d
kubectl -n argo get secrets argo-server-sso -o jsonpath="{.data.client-secret}" | base64 -d
```


## Installation

```bash
kubectl apply -f argo-workflows.yaml
```