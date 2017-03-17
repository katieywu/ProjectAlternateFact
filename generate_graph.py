import igraph as ig
import json
import urllib2
import plotly.plotly as py
from plotly.graph_objs import *


def generate_from_json(file_name):

    data = []
    # req = urllib2.Request("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json")
    # opener = urllib2.build_opener()
    # f = opener.open(req)
    # data = json.loads(f.read())
    with open(file_name) as json_file:
        data = json.load(json_file)

    N=len(data['nodes'])

    L=len(data['links'])
    print L
    Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

    G=ig.Graph(Edges, directed=True)
    # G = ig.Graph.Read_Ncol('../data/testpaolatiff_followers.txt', directed=True)

    labels=[]
    group=[]
    for node in data['nodes']:
        labels.append(node['name'])
        group.append(node['group'])

    layt=G.layout('kk', dim=3)

    Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
    Yn=[layt[k][1] for k in range(N)]# y-coordinates
    Zn=[layt[k][2] for k in range(N)]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for e in Edges:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]

    trace1=Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=Line(color='rgb(125,125,125)', width=1),
                   hoverinfo='none'
                   )
    trace2=Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode='markers',
                   name='actors',
                   marker=Marker(symbol='dot',
                                 size=6,
                                 color=group,
                                 colorscale='Viridis',
                                 line=Line(color='rgb(50,50,50)', width=0.5)
                                 ),
                   text=labels,
                   hoverinfo='text'
                   )


    axis=dict(showbackground=False,
              showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )

    layout = Layout(
             title="3D Twitter Follower Visualization",
             width=1000,
             height=1000,
             showlegend=False,
             scene=Scene(
             xaxis=XAxis(axis),
             yaxis=YAxis(axis),
             zaxis=ZAxis(axis),
            ),
         margin=Margin(
            t=100
        ),
        hovermode='closest'
    )

    data=Data([trace1, trace2])
    fig=Figure(data=data, layout=layout)
    # ig.plot(G)
    py.iplot(fig, filename='TestLarge')


def fake_test(seed_file, double_count_file):
    seeds = [line.rstrip('\n').split(' ', 1)[1] for line in open(seed_file, "r")]
    double_count = [line.rstrip('\n') for line in open(double_count_file, "r")]
    jsonwrapper = {}
    nodes = []
    links = []

    mapping = {}
    map_count = 0
    for account_name in seeds:
        mapping[account_name] = map_count
        nodes.append({"name": account_name, "group": 2})
        map_count += 1

    for double_val in double_count:
        source = map_count
        if double_val in mapping:
            source = mapping[double_val]
        else:
            map_count += 1
        for account_name in seeds:
                nodes.append({"name": str(account_name), "group": 1})
                links.append({"source": source, "target": mapping[account_name], "value": 1})
    jsonwrapper["nodes"] = nodes
    jsonwrapper["links"] = links
    with open('../data/doubleGraphRedState.txt', 'w') as outfile:
        json.dump(jsonwrapper, outfile)


fake_test("seeds.txt", "../data/doublecount_RedState.txt")
generate_from_json("../data/doubleGraphRedState.txt")
