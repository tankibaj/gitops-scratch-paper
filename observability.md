Table of Contents
=================

- [Consul](#consul)
    + [Deploy](#deploy)
    + [Clean up](#clean-up)
- [Monitoring stack](#monitoring-stack)
    * [Cortex](#cortex)
        + [Deploy](#deploy-1)
        + [Clean up](#clean-up-1)
    * [Prometheus Agent](#prometheus-agent)
        + [CRDs](#crds)
        + [Prometheus](#prometheus)
        + [Clean up](#clean-up-2)
- [Logging stack](#logging-stack)
    * [Loki](#loki)
    * [Promtail](#promtail)
    * [Clean up](#clean-up-3)


## Consul

Cortex and Loki require Key-Value store (KVS) to store the ring. It can use traditional KV stores like Consul or Etcd.

#### Deploy

```bash
kubectl apply -f consul.yaml
```

#### Clean up

```bash
kubectl delete -f consul.yaml
kubectl delete ns consul --force
```

<br/>

## Monitoring stack

### Cortex

[Cortex](https://github.com/cortexproject/cortex) provides horizontally scalable, highly available, multi-tenant, long term storage for Prometheus.

#### Deploy

```bash
kubectl apply -f cortex.yaml
```

#### Clean up

```bash
kubectl delete -f cortex.yaml
kubectl delete ns cortex --force
```

### Prometheus Agent

#### CRDs
The prometheus operator [CRDs](https://github.com/prometheus-operator/prometheus-operator#customresourcedefinitions)

```bash
kubectl apply -f prometheus-crds.yaml
```

#### Prometheus
The [kube-prometheus stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack), a collection of Kubernetes manifests, Grafana dashboards, and Prometheus rules combined with documentation and scripts to provide easy to operate end-to-end Kubernetes cluster monitoring with Prometheus using the Prometheus Operator.

```bash
kubectl apply -f prometheus-agent.yaml
```

#### Clean up

```bash
kubectl delete -f prometheus-crds.yaml
kubectl delete -f prometheus-crds/applicationset.yaml
kubectl delete -f prometheus-agent.yaml
kubectl delete -f prometheus-agent/applicationset.yaml
kubectl delete ns prometheus-agent --force
```

<br/>

## Logging stack

### Loki
[Loki](https://grafana.com/oss/loki/) is a horizontally scalable, highly available, multi-tenant log aggregation system inspired by Prometheus. It is designed to be very cost effective and easy to operate. It does not index the contents of the logs, but rather a set of labels for each log stream.

```bash
kubectl apply -f loki-distributed.yaml
```

### Promtail
[Promtail](https://grafana.com/docs/loki/latest/clients/promtail/) is an agent which ships the contents of local logs to a Grafana Loki instance.

```bash
kubectl apply -f promtail.yaml
```

### Clean up

```bash
kubectl delete -f loki-distributed.yaml
kubectl delete -f promtail.yaml
kubectl delete -f promtail/applicationset.yaml
kubectl delete ns loki --force
kubectl delete ns promtail --force
```

<br/>