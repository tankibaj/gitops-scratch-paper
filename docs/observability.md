# Observability stack
## Consul

Cortex and Loki require Key-Value store (KVS) to store the ring. It can use traditional KV stores like Consul or Etcd.

## Cortex

[Cortex](https://github.com/cortexproject/cortex) provides horizontally scalable, highly available, multi-tenant, long term storage for Prometheus.

#### Alert and Rule

- [Alertmanager](cortex-alert-rules/alertmanager.md)

- [Rules](cortex-alert-rules/rules.md)


## Prometheus
The [kube-prometheus stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack), a collection of Kubernetes manifests, Grafana dashboards, and Prometheus rules combined with documentation and scripts to provide easy to operate end-to-end Kubernetes cluster monitoring with Prometheus using the Prometheus Operator.

## Loki
[Loki](https://grafana.com/oss/loki/) is a horizontally scalable, highly available, multi-tenant log aggregation system inspired by Prometheus. It is designed to be very cost effective and easy to operate. It does not index the contents of the logs, but rather a set of labels for each log stream.

## Promtail
[Promtail](https://grafana.com/docs/loki/latest/clients/promtail/) is an agent which ships the contents of local logs to a Grafana Loki instance.

# Implementation

Deploy observability stack on cluster

```bash
kubectl apply -k observability.yaml
```