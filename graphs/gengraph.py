from grafanalib.core import *

def singleQueryGraph(title, exp, legend, yformat, ylabel, datasource):
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
                    expr=exp,
                    legendFormat=legend,
                    refId='A',
                ),
            ],
            xAxis=XAxis(mode="time"),
            yAxes=[
                YAxis(format=yformat, show=True, label=ylabel, min=0),
                YAxis(format=SHORT_FORMAT, show=True, min=None),
            ],
        )