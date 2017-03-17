import igraph

# load data into a graph
g = igraph.Graph(directed=True)
g.add_vertices(['paolaruano', 'tifffanyyyyy'])
g.add_edge("paolaruano", "tifffanyyyyy")

g.add_vertices(['hihi', 'nono'])
g.vs["type"] = [0, 0, 1, 1]


# for n in g.vs:
#     print n["value"]

print "test vert: " + str(g.vcount())

gOne = igraph.Graph.Read_Ncol('../data/testpaolatiff_followers.txt', directed=True)

# g = g.union(gtwo)


visual_style = {}

# Set bbox and margin
# visual_style["bbox"] = (800, 800)
# visual_style["margin"] = 100

# Don't curve the edges
# visual_style["edge_curved"] = False

# Community detection
# communities = g.community_edge_betweenness(directed=True)
# clusters = communities.as_clustering()
#
# # Set edge weights based on communities
# weights = {v: len(c) for c in clusters for v in c}
# g.es["weight"] = [weights[e.tuple[0]] + weights[e.tuple[1]] for e in g.es]
#
# # Choose the layout
# N = g.vcount()
# visual_style["layout"] = g.layout_bipartite(types="type", hgap=1, vgap=1, maxiter=100)

# Plot the graph
# igraph.plot(g, **visual_style)
igraph.plot(gOne)