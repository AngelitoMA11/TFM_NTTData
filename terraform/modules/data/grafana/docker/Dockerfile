FROM grafana/grafana:10.4.0

RUN grafana-cli plugins install grafana-bigquery-datasource

# Dashboard
COPY dashboards/dashboard.json /var/lib/grafana/dashboards/dashboard.json
COPY dashboards/dashboard2.json /var/lib/grafana/dashboards/dashboard2.json
COPY dashboards/oficina.json /var/lib/grafana/dashboards/oficina.json
COPY dashboards/principal.json /var/lib/grafana/dashboards/principal.json
COPY dashboards/prueba.json /var/lib/grafana/dashboards/prueba.json
COPY dashboards/epp.json /var/lib/grafana/dashboards/epp.json
COPY dashboards/cpt_interior.json /var/lib/grafana/dashboards/cpt_interior.json
COPY dashboards/mfs-ce.json /var/lib/grafana/dashboards/mfs-ce.json



# Provisioning
COPY provisioning/dashboards/dashboard.yaml /etc/grafana/provisioning/dashboards/dashboard.yaml
COPY provisioning/datasources/bigquery.yaml /etc/grafana/provisioning/datasources/bigquery.yaml
