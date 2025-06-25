FROM grafana/grafana:latest

RUN grafana-cli plugins install grafana-bigquery-datasource

# Dashboard
COPY dashboards/dashboard.json /var/lib/grafana/dashboards/dashboard.json

# Provisioning
COPY provisioning/dashboards/dashboard.yaml /etc/grafana/provisioning/dashboards/dashboard.yaml
COPY provisioning/datasources/bigquery.yaml /etc/grafana/provisioning/datasources/bigquery.yaml
