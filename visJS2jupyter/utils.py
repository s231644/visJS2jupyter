from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


# development versions of return_node_to_color and return_edge_to_color


def return_node_to_color(
        graph,
        field_to_map='degree',
        cmap=plt.get_cmap("jet"),
        alpha=1.0,
        color_vals_transform=None,
        ceil_val=10,
        color_max_frac=1.0,
        color_min_frac=0.0,
        vmin=None,
        vmax=None
):
    """
    Function to return a dictionary mapping nodes (keys) to colors (values), based on the selected field_to_map.
        - field_to_map must be a node attribute
        - cmap must be a valid matplotlib colormap
        - color_max_frac and color_min_frac allow user to set lower and upper ranges for colormap
    """

    nodes_with_data = [
        (node_id, node_data[field_to_map])
        for node_id, node_data in graph.nodes(data=True)
    ]
    nodes, data = zip(*nodes_with_data)

    if color_vals_transform == 'log':
        min_dn0 = np.nanmin([d for d in data if d > 0])
        data = [np.log(np.max([d, min_dn0])) for d in data]  # set the zero d values to minimum non0 value
        data = [(d - np.nanmin(data)) for d in data]  # shift so we don't have any negative values
        nodes_with_data = zip(nodes, data)

    elif color_vals_transform == 'sqrt':
        data = [np.sqrt(d) for d in data]
        nodes_with_data = zip(nodes, data)

    elif color_vals_transform == 'ceil':
        data = [min(d, ceil_val) for d in data]
        nodes_with_data = zip(nodes, data)
    else:
        pass

    # if vmin and vmax aren't set, set them to min and max of the data
    if vmin is None:
        vmin = np.nanmin(data)
    if vmax is None:
        vmax = np.nanmax(data)

    if vmin == vmax:
        vmax = vmax + 0.01

    node_to_map_field = dict(nodes_with_data)

    color_to_mult = 256 * (color_max_frac - color_min_frac)
    color_to_add = 256 * color_min_frac

    color_list = [
        np.multiply(
            cmap(
                int(
                    float(node_to_map_field[d] - vmin) / (vmax - vmin) * color_to_mult + color_to_add
                )
            ), 256
        ) if ~np.isnan(node_to_map_field[d]) else [np.nan]
        for d in graph.nodes()
    ]

    color_list = [
        (int(r), int(g), int(b), alpha) if ~np.isnan(r) else (200, 200, 200, alpha)
        for r, g, b, _ in color_list
    ]

    node_to_color = dict(zip(graph.nodes(), ['rgba' + str(c) for c in color_list]))

    return node_to_color


def return_edge_to_color(
        graph,
        field_to_map='degree',
        cmap=plt.get_cmap("jet"),
        alpha=1.0,
        color_vals_transform=None,
        ceil_val=10,
        vmin=None,
        vmax=None
):
    """
    Function to return a dictionary mapping edges (keys) to colors (values), based on the selected field_to_map.
        - field_to_map must be an edge attribute
        - cmap must be a valid matplotlib colormap
    """

    # if this is a multigraph or multidigraph, we need to keep track of keys
    is_multigraph = any([
        isinstance(graph, nx.classes.multigraph.MultiGraph),
        isinstance(graph, nx.classes.multidigraph.MultiDiGraph)
    ])

    if is_multigraph:
        edges_with_data = [
            (edge_from, edge_to, edge_keys, edge_data[field_to_map])
            for edge_from, edge_to, edge_keys, edge_data in graph.edges(keys=True, data=True)
        ]
        edges1, edges2, keys, data = zip(*edges_with_data)
        edges_with_data = zip(
            zip(edges1, edges2, keys),
            scale_data(data, color_vals_transform, ceil_val)
        )  # map edges to modified data
    # otherwise perform operations normally
    else:
        edges_with_data = [
            (edge_from, edge_to, edge_data[field_to_map])
            for edge_from, edge_to, edge_data in graph.edges(data=True)
        ]
        edges1, edges2, data = zip(*edges_with_data)
        edges_with_data = zip(
            zip(edges1, edges2),
            scale_data(data, color_vals_transform, ceil_val)
        )

    # if vmin and vmax aren't set, set them to min and max of the data
    if vmin is None:
        vmin = np.nanmin(data)
    if vmax is None:
        vmax = np.nanmax(data)

    # to avoid a "divide by zero" error
    if vmin == vmax:
        vmax = vmax + 0.01

    # if this is a multigraph or multidigraph, we need to keep track of keys
    if is_multigraph:
        edge_to_map_field = dict(edges_with_data)
        color_list = [
            np.multiply(
                cmap(
                    int(
                        float(edge_to_map_field[d] - vmin) / (vmax - vmin) * 256)
                ), 256
            ) for d in graph.edges(keys=True)
        ]
        color_list = [(int(r), int(r), int(b), alpha) for r, g, b in color_list]
        edge_to_color = dict(zip(graph.edges(keys=True), ['rgba' + str(c) for c in color_list]))
    else:
        edge_to_map_field = dict(edges_with_data)
        color_list = [
            np.multiply(
                cmap(
                    int(
                        float(edge_to_map_field[d] - vmin) / (vmax - vmin) * 256)
                ), 256
            ) for d in graph.edges()
        ]
        color_list = [(int(r), int(r), int(b), alpha) for r, g, b in color_list]
        edge_to_color = dict(zip(graph.edges(), ['rgba' + str(c) for c in color_list]))

    return edge_to_color


def scale_data(
        data,
        color_vals_transform=None,
        ceil_val=10,
):
    if color_vals_transform == 'log':  # log(data)
        data = [np.log(d) for d in data]
        data = [(d - np.min(data)) for d in data]  # shift so we don't have any negative values
    elif color_vals_transform == 'sqrt':  # sqrt(data)
        data = [np.sqrt(d) for d in data]
    elif color_vals_transform == 'ceil':  # ceil(data)
        data = [max(d, ceil_val) for d in data]
    return data
