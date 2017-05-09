import plotly.plotly as py
import plotly.graph_objs as go
import numpy
import scipy
import make_sketch as ms

"""
Given a text file where each line is a number + \n,
outputs a bar graph based on the frequency for which each packet per second value occurs to sho the distribution.
"""
def graph_pps(outfile):
    sketch = {}
    with open('pps.txt', 'r') as f:
        while True:
            second = f.readline()
            if second == '':
                break
            sketch = ms.make_sketch(sketch, second[:2])
    sort = sorted(iter(sketch))
    total = 0
    percents = []
    pps = []
    for i in range(0, len(sort)):
        total += sketch[sort[i]]
        pps.append(int(sort[i]))
    for i in range(0, len(sort)):
        percents.append(round((sketch[sort[i]] / total) * 100, 1))
    print(percents)
    data = [go.Scatter(x=pps, y=percents, marker=dict(color="rgb(16, 32, 77)")),
            go.Bar(x=pps, y=percents, name="% Packets")]
    layout = go.Layout(title="Average Packets Per Second", xaxis=dict(title="Packets Per Second"),
        annotations=[dict(text="", x=0, xref="paper", y=0, yref="paper")])
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename=outfile)