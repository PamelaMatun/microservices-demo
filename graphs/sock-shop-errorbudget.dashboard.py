import itertools
import operator
import os

from grafanalib.core import *

def service_row(datasource, serviceTitle, serviceName):
    return Row(
        title=serviceTitle,
        showTitle=True,
        panels=[
            service_error_budget(datasource, serviceTitle, serviceName),
        ],
    )

def service_error_budget(datasource, serviceTitle, serviceName):
    title = serviceTitle + " Error Budget"
    return Graph(
        title=title,
        dataSource=datasource,
        span=6,
        lineWidth=1,
        legend=Legend(
            show=True,
            alignAsTable=True,
        ),
        targets=[
            Target(
                expr='(1-(sum(increase(request_duration_seconds_count{name="%s",status_code=~"4.+|5.+"}[5h]))/sum(increase(request_duration_seconds_count{name="%s"}[5h])))/(1 - .80))*100' % (serviceName, serviceName)
                legendFormat="error budget",
                refId='A',
            ),
        ],
        xAxis=XAxis(mode="time"),
        yAxes=[
            YAxis(format=PERCENT_FORMAT, show=True, label="Error Budget(5h)", min=0),
            YAxis(format=SHORT_FORMAT, show=True, min=None),
        ],
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
    title="Sock Shop Error Budget",
    time=Time("now-30m", "now"),
    timezone="browser",
    refresh="5s",
    rows=rows,
).auto_panel_ids()
