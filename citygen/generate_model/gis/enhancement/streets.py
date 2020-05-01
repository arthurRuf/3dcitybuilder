import osmnx as ox

# https://geoffboeing.com/2016/11/osmnx-python-street-networks/

def retrieve_street_layer(mission_shape):
    G = ox.graph_from_polygon(mission_shape, network_type='drive')
    ox.plot_graph(G)
