import itertools
import operator
import os

from grafanalib.core import *
from gengraph import *

def service_row(datasource, serviceTitle, serviceName):
    return Row(
        title=serviceTitle,
        showTitle=True,
        panels=[
            service_qps_graph(datasource, serviceTitle, serviceName),
            service_latency_graph(datasource, serviceTitle, serviceName),
            service_error_budget(datasource, serviceTitle, serviceName),
        ],
    )
def service_qps_graph(datasource, serviceTitle, serviceName):
    title = serviceTitle + " QPS"
    expr='sum(rate(request_duration_seconds_count{name="%s",route!="metrics"}[1m])) by(status_code) * 100' % (serviceName)
    legendFormat="{{ status_code }}"
    yformat=OPS_FORMAT
    ylabel="QPS (1 min)"
    return singleQueryGraph(
        title,
        expr,
        legendFormat,
        yformat,
        ylabel,
        datasource
        )
def service_latency_graph(datasource, serviceTitle, serviceName):
    title = serviceTitle + " Latency (P99)"
    expr='histogram_quantile(0.99, sum(rate(request_duration_seconds_bucket{name="%s"}[1m])) by (name, le))' % (serviceName)
    legendFormat="99th quantile"
    yformat=SECONDS_FORMAT
    ylabel="latency"
    return singleQueryGraph(
        title,
        expr,
        legendFormat,
        yformat,
        ylabel,
        datasource
        )
def service_error_budget(datasource, serviceTitle, serviceName):
    title = serviceTitle + " Error Budget"
    expr='(1-(sum(increase(request_duration_seconds_count{name="%s",status_code=~"4.+|5.+"}[5h]))/sum(increase(request_duration_seconds_count{name="%s"}[5h])))/(1 - .80))*100' % (serviceName, serviceName)
    legendFormat="budget"
    yformat=PERCENT_FORMAT
    ylabel="Error Budget(5h)"
    return singleQueryGraph(
        title,
        expr,
        legendFormat,
        yformat,
        ylabel,
        datasource
        )

datasource = "prometheus"
rows = []
services = [
        {"name": "catalogue", "title": "Catalogue"},
        {"name": "carts", "title": "Cart"},
        {"name": "orders", "title": "Orders"},
        {"name": "payment", "title": "Payment"},
        {"name": "shipping", "title": "Shipping"},
        {"name": "user", "title": "User"},
        {"name": "front-end", "title": "Front End"},
]

for service in services:
    rows.append(service_row(datasource, service["title"], service["name"]))

dashboard = Dashboard(
    title="Sock Shop RED",
    time=Time("now-30m", "now"),
    timezone="browser",
    refresh="5s",
    rows=rows,
).auto_panel_ids()