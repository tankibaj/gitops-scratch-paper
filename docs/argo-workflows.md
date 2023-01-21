## Overview
Argo Workflows is an open source container-native workflow engine for orchestrating parallel jobs on Kubernetes. Argo Workflows is implemented as a Kubernetes CRD (Custom Resource Definition).

## Prerequisite
Create a Kubernetes secrets to store the OAuth2 `client-id` and `client-secret` for Argo Server SSO.

```bash
kubectl create secret -n argo generic argo-server-sso \
  --from-literal=client-id=argo-workflows \
  --from-literal=client-secret=<client secret>
```

## Installation

```bash
kubectl apply -f ../argo-workflows.yaml
```