FROM grafana/grafana:latest

RUN grafana-cli plugins install grafana-bigquery-datasource

# Dashboard
COPY dashboards/dashboard.json /var/lib/grafana/dashboards/dashboard.json
COPY dashboards/accuracy-interior.json /var/lib/grafana/dashboards/accuracy-interior.json
COPY dashboards/cpt_interior.json /var/lib/grafana/dashboards/cpt_interior.json
COPY dashboards/mfs-interior.json /var/lib/grafana/dashboards/mfs-interior.json
COPY dashboards/ept_interior.json /var/lib/grafana/dashboards/ept_interior.json
COPY dashboards/dws-interior.json /var/lib/grafana/dashboards/dws-inteior.json
COPY dashboards/cambios.json /var/lib/grafana/dashboards/cambios.json
COPY dashboards/ce-interior.json /var/lib/grafana/dashboards/ce-interior.json
COPY dashboards/epp.json /var/lib/grafana/dashboards/epp.json




# Provisioning
COPY provisioning/dashboards/dashboard.yaml /etc/grafana/provisioning/dashboards/dashboard.yaml
COPY provisioning/datasources/bigquery.yaml /etc/grafana/provisioning/datasources/bigquery.yaml
