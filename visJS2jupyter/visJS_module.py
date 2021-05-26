"""
--------------------------------------------------------

Authors:
    - Brin Rosenthal (sbrosenthal@ucsd.edu)
    - Aaron Gary (agary@ucsd.edu)
    - Mikayla Webster (13webstermj@gmail.com)

--------------------------------------------------------
"""

# import some packages
from __future__ import print_function
from IPython.display import HTML, Javascript
from json import dumps
import networkx as nx

Javascript("$.getScript('https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.js')")


def visjs_network(
        nodes_dict,
        edges_dict,

        # by node
        node_border_width=2,  # node border width when not hover or selected
        node_border_width_selected=2,  # node border width once clicked
        node_broken_image='undefined',  # back-up image in case a node image doesn't successfully load
        node_color_border='black',  # creates border around node shape
        node_color_highlight_border='#2B7CE9',  # node border color when selected
        node_color_highlight_background='orange',  # border color when selected
        node_color_hover_border='#2B7CE9',  # color of node border when mouse hovers but does not click
        node_color_hover_background='orange',  # color of node when mouse hovers but does not click
        node_fixed_x=False,  # node does not move in x direction but is still calculated into physics
        node_fixed_y=False,  # node does not move in y direction but is still calculated into physics
        node_font_color='#343434',  # color of label text
        node_font_size=14,  # size of label text
        node_font_face='arial',  # font face of label text
        node_font_background="rgba(0,0,0,0)",
        # when defined with color string, a background rectangle will be drawn around text
        node_font_stroke_width=0,  # width of stroke, if zero not drawn
        node_font_stroke_color='#ffffff',  # color of stroke
        node_font_align='center',  # other option is 'left'
        node_icon_face='FontAwesome',  # only used when shape is set to icon. Options are 'FontAwesome' and 'Ionicons'
        node_icon_code='undefined',  # code used to define which icon to use
        node_icon_size=50,  # size of icon
        node_icon_color='#2B7CE9',  # color of icon
        node_image='undefined',
        # when shape set to 'image' or 'circularImage', then the URL image designated here will be used
        node_label_highlight_bold=True,  # determines if label boldens when node is selected
        node_scaling_min=10,  # min size node can become when it scales down
        node_scaling_max=30,  # max size node can become when it scales up
        node_scaling_label_enabled=False,  # toggle scaling of label on or off
        node_scaling_label_min=14,  # min font size the label can become when it scales down
        node_scaling_label_max=30,  # max font size the label can become when it scales up
        node_scaling_label_max_visible=30,  # font will never be larger than this number at 100% zoom
        node_scaling_label_draw_threshold=5,
        # lower limit font is drawn as, use this and max visible to control which labels remain visible during zoom out
        node_shadow_enabled=True,  # whether there is a shadow cast by the nodes
        node_shadow_color='rgba(0,0,0,0.5)',  # shadow color
        node_shadow_size=10,  # shadow blur size
        node_shadow_x=5,  # shadow x offset from node
        node_shadow_y=5,  # shadow y offset from node
        node_shape_border_dashes=False,  # makes dashed border around node
        node_shape_border_radius=6,  # determines roundness of node shape (only for "box" shape)
        node_shape_interpolation=True,  # only for image and circular image: image resamples when scaling down
        node_shape_use_image_size=False,
        # only for image and circular image: true means use image size, false use our defined node size
        node_shape_use_border_with_image=False,  # only for image: draws border around image icon
        node_label_field='id',  # field that nodes will be labeled with
        node_size_field='degree',  # field that determines which nodes are more important thus should be scaled bigger
        node_size_transform='Math.sqrt',
        # function by which higher value (not node_value) nodes are scaled larger to show importance
        node_size_multiplier=3,
        # increment by which higher value (not node_value) nodes are scaled larger to show importance

        # by edge
        edge_title_field='id',  # which attribute name to show on edge hover
        edge_arrow_to=False,  # creates a directed edge with arrow head on receiving node
        edge_arrow_from=False,  # creates a directed edge with arrow head coming from delivering node
        edge_arrow_middle=False,  # creates a directed edge where arrow is in center of edge
        edge_arrow_to_scale_factor=1,  # changes size of to arrow head
        edge_arrow_from_scale_factor=1,  # changes size of from arrow head
        edge_arrow_middle_scale_factor=1,  # changes size of middle arrow head
        edge_arrow_strikethrough=True,  # when False, edge stops at arrow
        edge_color='#848484',
        # if all edges are to be a single color, specify here. Empty string refers edge color to each individual object
        edge_color_highlight='#848484',  # same but for highlight color
        edge_color_hover='#848484',  # same but for hover color
        edge_color_inherit='from',
        # if edge color is set, must be false. Else inherits color from "to", "from", or "both" connected nodes
        edge_color_opacity=1.0,  # number from 0 - 1 that sets opacity of all edge colors
        edge_dashes=False,  # if true, edges will be drawn with a dashed line
        edge_font_color='#343434',  # color of label text
        edge_font_size=20,  # size of label text
        edge_font_face='ariel',  # font of label text
        edge_font_background='rgba(0,0,0,0)',
        # when given a color string, a background rectangle of that color will be drawn behind the label
        edge_font_stroke_width=0,  # stroke drawn around text
        edge_font_stroke_color='#343434',  # color of stroke
        edge_font_align='horizontal',  # 'horizontal', 'middle', 'top', or 'bottom'
        edge_hover_width=0.5,  # number to be added to width of edge to determine hovering
        edge_label_highlight_bold=True,  # determines whether label becomes bold when edge is selected
        edge_length='undefined',  # when a number is defined the edges' spring length is overridden
        edge_scaling_min=1,  # minimum allowed edge width value
        edge_scaling_max=15,  # maximum allowed edge width value
        edge_scaling_label_enabled=False,  # when true, the label will scale with the edge width
        edge_scaling_label_min=14,  # min font size used for labels when scaling
        edge_scaling_label_max=30,  # max font size used for labels when scaling
        edge_scaling_label_max_visible=30,  # max font size of label will zoom in
        edge_scaling_label_draw_threshold=5,  # min font size of label when zooming out
        edge_selection_width=1,  # number added to width when determining if edge is selected
        edge_self_reference_size=10,  # when there is a self-loop, this is the radius of that circle
        edge_shadow_enabled=False,  # whether or not shadow is cast
        edge_shadow_color='rgba(0,0,0,0.5)',  # color of shadow as a string
        edge_shadow_size=10,  # blur size of shadow
        edge_shadow_x=5,  # x offset
        edge_shadow_y=5,  # y offset
        # if this is set to true and smooth type is not continuous, you will not be able to set the x and y position
        edge_smooth_enabled=False,  # toggle smoothed curves
        edge_smooth_type='dynamic',
        edge_smooth_force_direction='none',  # 'horizontal', 'vertical', and 'none'. Only for cubicBezier curves
        edge_smooth_roundness=0.5,  # number between 0 and 1 that changes roundness of curve except with dynamic curves
        edge_width=1,  # width of all edges
        edge_label_field="id",
        edge_width_field="",  # empty string will use global value for all edge widths

        # interaction
        drag_nodes=True,  # When true, the nodes that are not fixed can be dragged by the user.
        drag_view=True,  # When true, the view can be dragged around by the user.
        hide_edges_on_drag=False,  # When true, the edges are not drawn when dragging the view.
        # This can greatly speed up responsiveness on dragging, improving user experience.
        hide_nodes_on_drag=False,  # When true, the nodes are not drawn when dragging the view.
        # This can greatly speed up responsiveness on dragging, improving user experience.
        hover=True,  # When true, the nodes use their hover colors when the mouse moves over them.
        hover_connected_edges=True,  # When true, on hovering over a node, it's connecting edges are highlighted.
        keyboard_enabled=False,  # Toggle the usage of the keyboard shortcuts. If this option is not defined,
        # it is set to true if any of the properties in this object are defined.
        keyboard_speed_x=10,
        # The speed at which the view moves in the x direction on pressing a key or pressing a navigation button.
        keyboard_speed_y=10,
        # The speed at which the view moves in the y direction on pressing a key or pressing a navigation button.
        keyboard_speed_zoom=0.02,
        # The speed at which the view zooms in or out pressing a key or pressing a navigation button.
        keyboard_bind_to_window=True,
        # When binding the keyboard shortcuts to the window, they will work regardless of which DOM object
        # has the focus. If you have multiple networks on your page, you could set this to false, making sure
        # the keyboard shortcuts only work on the network that has the focus.
        multiselect=False,
        # When true, a longheld click (or touch) as well as a control-click will add to the selection.
        navigation_buttons=False,
        # When true, navigation buttons are drawn on the network canvas.
        # These are HTML buttons and can be completely customized using CSS.
        selectable=True,  # When true, the nodes and edges can be selected by the user.
        select_connected_edges=True,  # When true, on selecting a node, its connecting edges are highlighted.
        tooltip_delay=300,
        # When nodes or edges have a defined 'title' field, this can be shown as a pop-up tooltip.
        # The tooltip itself is an HTML element that can be fully styled using CSS. The delay is the amount of time
        # in milliseconds it takes before the tooltip is shown.
        zoom_view=True,  # When true, the user can zoom in.

        # configuration
        config_enabled=False,
        # Toggle the configuration interface on or off. This is an optional parameter. If left undefined and any
        # of the other properties of this object are defined, this will be set to true.
        config_filter="nodes,edges",
        # When a string is supplied, any combination of the following is allowed: nodes, edges, layout, interaction,
        # manipulation, physics, selection, renderer. Feel free to come up with a fun seperating character.
        # Finally, when supplied an array of strings, any of the previously mentioned fields are accepted.
        container="undefined",
        # This allows you to put the configure list in another HTML container than below the network.
        show_button=False,  # Show the generate options button at the bottom of the configurator.

        # other stuff
        border_color='white',
        physics_enabled=False,
        min_velocity=2,
        max_velocity=8,
        draw_threshold=None,
        min_label_size=None,
        max_label_size=None,
        max_visible=None,
        graph_title='',
        graph_width=900,
        graph_height=800,
        scaling_factor=1,
        time_stamp=0,  # deprecated: use graph_id
        graph_id=0,  # To draw multiple graphs in the same notebook, give each a different id
        export_network=False,
        export_file='network.json',
        override_graph_size_to_max=False,
        output="jupyter",
):
    """
    This function creates an iframe for the input graph

    Inputs:
        - nodes_dict: dictionary of nodes and attributes
        - edges_dict: dictionary of edges and attributes
        - visJS_html_file:  path to visJS_html style file (from create_graph_style_file)

    Return:
        - VisJS html network plot (iframe)

    """

    # error checking for nodes_dict and edges_dict
    if not nodes_dict:
        print("Error: nodes_dict is empty")
        return

    if type(nodes_dict[0]) is not dict:
        print("Error: nodes_dict does not contain dictionary")
        return

    if 'id' not in nodes_dict[0].keys():
        print("Error: 'id' must be in nodes_dict")
        return

    if 'x' not in nodes_dict[0].keys():
        print("Error: 'x' must be in nodes_dict")
        return

    if 'y' not in nodes_dict[0].keys():
        print("Error: 'y' must be in nodes_dict")
        return

    if not edges_dict:
        print("Error: edges_dict is empty")
        return

    if type(edges_dict[0]) is not dict:
        print("Error: edges_dict does not contain dictionary")
        return

    if 'source' not in edges_dict[0].keys():
        print("Error: 'source' must be in edges_dict")
        return

    if 'target' not in edges_dict[0].keys():
        print("Error: 'target' must be in edges_dict")
        return

    # turn off physics simulation if scaling graph
    if scaling_factor > 1:
        physics_enabled = False

    # checking for deprecated arguments
    if time_stamp > 0:
        graph_id = time_stamp

    if draw_threshold is not None:
        node_scaling_label_draw_threshold = draw_threshold
        edge_scaling_label_draw_threshold = draw_threshold

    if min_label_size is not None:
        node_scaling_label_min = min_label_size
        edge_scaling_label_min = min_label_size

    if max_label_size is not None:
        node_scaling_label_max = max_label_size
        edge_scaling_label_max = max_label_size

    if max_visible is not None:
        node_scaling_label_max_visible = max_visible
        edge_scaling_label_max_visible = max_visible

    # check nodes_dict and edges_dict and fill in default values
    nodes_dict = check_nodes_dict(nodes_dict)

    if export_network:
        export_to_cytoscape(
            nodes_dict=nodes_dict,
            edges_dict=edges_dict,
            export_file=export_file,
        )

    physics_enabled = stringify_bool(physics_enabled)
    edge_arrow_to = stringify_bool(edge_arrow_to)
    edge_arrow_from = stringify_bool(edge_arrow_from)
    edge_arrow_middle = stringify_bool(edge_arrow_middle)
    edge_arrow_strikethrough = stringify_bool(edge_arrow_strikethrough)
    edge_dashes = stringify_bool(edge_dashes)
    edge_label_highlight_bold = stringify_bool(edge_label_highlight_bold)
    edge_scaling_label_enabled = stringify_bool(edge_scaling_label_enabled)
    edge_shadow_enabled = stringify_bool(edge_shadow_enabled)
    edge_smooth_enabled = stringify_bool(edge_smooth_enabled)
    node_fixed_x = stringify_bool(node_fixed_x)
    node_fixed_y = stringify_bool(node_fixed_y)
    node_label_highlight_bold = stringify_bool(node_label_highlight_bold)
    node_scaling_label_enabled = stringify_bool(node_scaling_label_enabled)
    node_shadow_enabled = stringify_bool(node_shadow_enabled)
    node_shape_border_dashes = stringify_bool(node_shape_border_dashes)
    node_shape_interpolation = stringify_bool(node_shape_interpolation)
    node_shape_use_image_size = stringify_bool(node_shape_use_image_size)
    node_shape_use_border_with_image = stringify_bool(node_shape_use_border_with_image)
    drag_nodes = stringify_bool(drag_nodes)
    drag_view = stringify_bool(drag_view)
    hide_edges_on_drag = stringify_bool(hide_edges_on_drag)
    hide_nodes_on_drag = stringify_bool(hide_nodes_on_drag)
    hover = stringify_bool(hover)
    hover_connected_edges = stringify_bool(hover_connected_edges)
    keyboard_enabled = stringify_bool(keyboard_enabled)
    keyboard_bind_to_window = stringify_bool(keyboard_bind_to_window)
    multiselect = stringify_bool(multiselect)
    navigation_buttons = stringify_bool(navigation_buttons)
    selectable = stringify_bool(selectable)
    select_connected_edges = stringify_bool(select_connected_edges)
    zoom_view = stringify_bool(zoom_view)
    config_enabled = stringify_bool(config_enabled)
    show_button = stringify_bool(show_button)

    graph_width = scaling_factor * graph_width
    graph_height = scaling_factor * graph_height
    if edge_length != 'undefined':
        edge_length *= scaling_factor
    if override_graph_size_to_max:
        graph_width = "100%"
        graph_height = "100%"
        frame_max = """
        html, body {
          width: 100%;
          height: 100%;
        }"""
    else:
        graph_width = "{}px".format(graph_width)
        graph_height = "{}px".format(graph_height)
        frame_max = ""

    external = """
  {}<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css"/>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.12.2/d3.min.js" type="text/javascript"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.js"></script>
    """.format(
        """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css"/>\n"""
        if output in ["jupyter", "html"] else ""
    )

    style = frame_max + """
    #mynetwork""" + str(graph_id) + """ {
      width: """ + graph_width + """;
      height: """ + graph_height + """;
      border: 5px solid """ + border_color + """;
      box-sizing: border-box;
    }
    """

    network_div = """
  <div id="mynetwork{}"></div>""".format(graph_id)

    run_vis = """
    function runVis(visNodes, visEdges) {
       var vizOptions = {
          configure: {
            enabled: """ + config_enabled + """,
            filter: '""" + config_filter + """',
            container: """ + container + """,
            showButton: """ + show_button + """
          },
          edges:{
            arrows: {
               to:     {enabled: """ + edge_arrow_to + """, scaleFactor:""" + str(edge_arrow_to_scale_factor) + """},
               middle:   {enabled: """ + edge_arrow_middle + """, scaleFactor:""" + str(
        edge_arrow_middle_scale_factor) + """},
               from: {enabled: """ + edge_arrow_from + """, scaleFactor:""" + str(edge_arrow_from_scale_factor) + """}
            },
            arrowStrikethrough: """ + edge_arrow_strikethrough + """,
            color: {
               color: '""" + edge_color + """',
               highlight: '""" + edge_color_highlight + """',
               hover: '""" + edge_color_hover + """',
               inherit: '""" + edge_color_inherit + """',
               opacity: """ + str(edge_color_opacity) + """
            },
            dashes: """ + edge_dashes + """,
            font: {
                color: '""" + edge_font_color + """',
                size: """ + str(edge_font_size) + """*""" + str(scaling_factor) + """,
                face: '""" + edge_font_face + """',
                background: '""" + edge_font_background + """',
                strokeWidth: """ + str(edge_font_stroke_width) + """,
                strokeColor: '""" + edge_font_stroke_color + """',
                align:'""" + edge_font_align + """'
            },
            hoverWidth: """ + str(edge_hover_width) + """,
            labelHighlightBold: """ + edge_label_highlight_bold + """,
            length: """ + str(edge_length) + """,
            scaling:{
               min: """ + str(edge_scaling_min) + """,
               max: """ + str(edge_scaling_max) + """,
               label: {
                  enabled: """ + edge_scaling_label_enabled + """,
                  min: """ + str(edge_scaling_label_min) + """,
                  max: """ + str(edge_scaling_label_max) + """*""" + str(scaling_factor) + """,
                  maxVisible: """ + str(edge_scaling_label_max_visible) + """*""" + str(scaling_factor) + """,
                  drawThreshold: """ + str(edge_scaling_label_draw_threshold) + """,
               }
            },
            selectionWidth: """ + str(edge_selection_width) + """,
            selfReferenceSize: """ + str(edge_self_reference_size) + """,
            shadow:{
               enabled: """ + edge_shadow_enabled + """,
               color: '""" + edge_shadow_color + """',
               size: """ + str(edge_shadow_size) + """,
               x: """ + str(edge_shadow_x) + """,
               y: """ + str(edge_shadow_y) + """
            },
            smooth: {
               enabled: """ + edge_smooth_enabled + """,
               type: '""" + edge_smooth_type + """',
               forceDirection: '""" + edge_smooth_force_direction + """',
               roundness: """ + str(edge_smooth_roundness) + """
            },
            width: """ + str(edge_width) + """*""" + str(scaling_factor) + """,
          },
          interaction:{
            dragNodes: """ + drag_nodes + """,
            dragView: """ + drag_view + """,
            hideEdgesOnDrag: """ + hide_edges_on_drag + """,
            hideNodesOnDrag: """ + hide_nodes_on_drag + """,
            hover: """ + hover + """,
            hoverConnectedEdges: """ + hover_connected_edges + """,
            keyboard: {
                enabled: """ + keyboard_enabled + """,
                speed: {x: """ + str(keyboard_speed_x) + """, y: """ + str(keyboard_speed_y) + """, zoom: """ + str(
        keyboard_speed_zoom) + """},
                bindToWindow: """ + keyboard_bind_to_window + """
            },
            multiselect: """ + multiselect + """,
            navigationButtons: """ + navigation_buttons + """,
            selectable: """ + selectable + """,
            selectConnectedEdges: """ + select_connected_edges + """,
            tooltipDelay: """ + str(tooltip_delay) + """,
            zoomView: """ + zoom_view + """
          },
          layout: {
            improvedLayout:true,
            hierarchical: {
                enabled:false,
                levelSeparation: 150,
                direction: 'UD',
                sortMethod: 'hubsize'
            },
            randomSeed: 780555
          },
          nodes: {
              borderWidth: """ + str(node_border_width) + """,
              borderWidthSelected: """ + str(node_border_width_selected) + """,
              brokenImage: '""" + node_broken_image + """',
              color: {
                 border: '""" + node_color_border + """',
                 highlight: {
                    background: '""" + node_color_highlight_background + """',
                    border: '""" + node_color_highlight_border + """'
                 },
                 hover: {
                    background: '""" + node_color_hover_background + """',
                    border: '""" + node_color_hover_border + """'
                 }
              },
              font: {
                 color: '""" + node_font_color + """',
                 size: """ + str(node_font_size) + """*""" + str(scaling_factor) + """,
                 face: '""" + node_font_face + """',
                 background: '""" + node_font_background + """',
                 strokeWidth: """ + str(node_font_stroke_width) + """,
                 strokeColor: '""" + node_font_stroke_color + """',
                 align: '""" + node_font_align + """'
              },
              icon: {
                 face: '""" + node_icon_face + """',
                 code: """ + node_icon_code + """,
                 size: """ + str(node_icon_size) + """,
                 color:'""" + node_icon_color + """'
              },
              image: {
                 unselected: '""" + node_image + """',
                 selected: '""" + node_image + """'
              },
              labelHighlightBold: """ + node_label_highlight_bold + """,
              scaling: {
                 min: """ + str(node_scaling_min) + """,
                 max: """ + str(node_scaling_max) + """,
                 label: {
                     enabled: """ + node_scaling_label_enabled + """,
                     min: """ + str(node_scaling_label_min) + """,
                     max: """ + str(node_scaling_label_max) + """*""" + str(scaling_factor) + """,
                     maxVisible: """ + str(node_scaling_label_max_visible) + """*""" + str(scaling_factor) + """,
                     drawThreshold: """ + str(node_scaling_label_draw_threshold) + """
                 }
              },
              shadow:{
                 enabled: """ + node_shadow_enabled + """,
                 color: '""" + node_shadow_color + """',
                 size:""" + str(node_shadow_size) + """,
                 x: """ + str(node_shadow_x) + """,
                 y: """ + str(node_shadow_y) + """
              },
              shapeProperties: {
                 borderDashes: """ + node_shape_border_dashes + """, // only for borders
                 borderRadius: """ + str(node_shape_border_radius) + """,     // only for box shape
                 interpolation: """ + node_shape_interpolation + """,  // only for image and circularImage shapes
                 useImageSize: """ + node_shape_use_image_size + """,  // only for image and circularImage shapes
                 useBorderWithImage: """ + node_shape_use_border_with_image + """  // only for image shape
              }
          },
         physics: {
            enabled: """ + physics_enabled + """,
            stabilization: false,
            barnesHut: {gravitationalConstant: -8000, springConstant: 0.012, springLength: 100},
            maxVelocity: """ + str(max_velocity) + """,
            minVelocity: """ + str(min_velocity) + """,
            solver: 'barnesHut',
            adaptiveTimestep: true,
            stabilization: {
              enabled: true,
              iterations: 1000,
              updateInterval: 100,
              onlyDynamicEdges: false,
              fit: true
            }
          }
       };
       var python_nodes = visNodes;
       var nodeArray = [];
       for(var i=0; i<python_nodes.length; i++){
         var node_degree = python_nodes[i].degree > 30 ? 30 + ((python_nodes[i].degree - 30)/6) : python_nodes[i].degree;
         node_degree = node_degree < 10 ? 10 : node_degree;
         var font_size = python_nodes[i].degree * 2;
         font_size = font_size < 10 ? 10 : font_size;
         nodeArray.push({id: i,
                         label: python_nodes[i].""" + node_label_field + """,
                         borderWidth: python_nodes[i].border_width * """ + str(scaling_factor) + """,
                         borderWidthSelected: """ + str(node_border_width_selected) + """,
                         color: {
                             background: python_nodes[i].color,
                             border: python_nodes[i].border_color,
                             hover: {
                                border: python_nodes[i].border_color_hover,
                             },
                         },
                         title: python_nodes[i].title,
                         shape: python_nodes[i].node_shape,
                         size: """ + node_size_transform + """(python_nodes[i].""" + node_size_field + """)*""" + str(
        node_size_multiplier) + """*""" + str(scaling_factor) + """,
                         x: python_nodes[i].x * """ + str(scaling_factor) + """,
                         y: python_nodes[i].y * """ + str(scaling_factor) + """});
         }
       var python_edges = visEdges;
       var edgeArray = [];
       for(var i=0; i<python_edges.length; i++){
         edgeArray.push({from: python_edges[i].source,
                         to: python_edges[i].target,
                         label: python_edges[i].""" + edge_label_field + """,
                         title: python_edges[i].""" + edge_title_field + """,
                         color: {
                            color: python_edges[i].color,
                            opacity: """ + str(edge_color_opacity) + """
                        },
                         width: """ + (
                  "python_edges[i].{} * {}".format(edge_width_field,
                                                   scaling_factor) if edge_width_field else "null") + """
            });
       }
       //console.log(nodeArray);
       //console.log(edgeArray);
       var vis_nodes = new vis.DataSet(nodeArray);
       var vis_edges = new vis.DataSet(edgeArray);

        var container = document.getElementById('mynetwork""" + str(graph_id) + """');
        var data = {
            edges: vis_edges,
            nodes: vis_nodes
        };
        var options = {};
        var myNetwork = new vis.Network(container, data, vizOptions);

        myNetwork.fit();


       console.log( "ready!" );
    }
    """

    visJS_to_write = """<!doctype html>
    <html>
    <head>
      <title>Network | Basic usage</title>
        """ + external + """
      <style type="text/css">
        """ + style + """
      </style>
    </head>
    <body onload="init();">

    <p>
      """ + graph_title + """
    </p>

      """ + network_div + """

    <script type="text/javascript">

        function setUpFrame() {
          runVis(""" + dumps(nodes_dict) + ', ' + dumps(edges_dict) + ');' + """
        }

        function init() { setUpFrame(); return true; }
      """ + run_vis + """
    </script>

        </body>
    </html>
        """

    if output == "jupyter":
        html_return = HTML(visJS_to_write)
        return html_return
    elif output == "html":
        return visJS_to_write
    else:
        result = {
            "external": external,
            "style": style,
            "script": run_vis,
            "run": "setUpFrame();",
            "body": network_div,
        }

    script = """
        {}
        function setUpFrame() {{
          window.runVis({}, {});
        }}{}
      """.format(result["script"], dumps(nodes_dict), dumps(edges_dict),
                 (("\n" + result["run"]) if output == "zeppelin" else ""))
    head = """
        {}
        <style type="text/css">
        {}
        </style>
        <script type="text/javascript">
        {}
        </script>
      """.format(result["external"], result["style"], script)
    if output == "zeppelin":
        return """%html
        {}
        {}
        """.format(result["body"], head)
    elif output == "div":
        return {
            "external": result["external"],
            "style": result["style"],
            "script": script,
            "run": result["run"],
            "body": result["body"],
        }


def export_to_cytoscape(
        nodes_dict=None,
        edges_dict=None,
        G=None,
        export_file='network.json'
):
    """
    SBR updated 12/19/17 to rectify error in handling of the 'id' field

    Exports graph to JSON file in a Cytoscape compatible format.

    Inputs:
        - nodes_dict: dictionary of nodes and attributes
        - edges_dict: dictionary of edges and attributes
        - G: a networkX graph to use in place of nodes and edges dicts
        - export_file: JSON file name to export graph to
        - export_node_attribute: currently unsupported
        - export_edge_attribute: currently unsupported
    """

    if nodes_dict is None and edges_dict is None and G is None:
        print(
            'Please specify either a networkX graph (G) or a nodes_dict and edges_dict '
            'when calling visJS_module.export_to_cytoscape'
        )
        return -1

    if (nodes_dict is None) or (edges_dict is None):
        print(
            'Please specify both a nodes_dict and edges_dict '
            'when calling visJS_module.export_to_cytoscape'
        )
        return -1

    # if the user did not specify a graph
    if G is None:
        # making the basic graph from only node id
        nodes = [node['id'] for node in nodes_dict]  # nodes_dict must contain id
        node_map = dict(zip(nodes, range(len(nodes))))  # relabel ids so they match the edges
        edges = [(edge['source'], edge['target']) for edge in edges_dict]
        # edges_dict must contain source and target
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G = nx.relabel_nodes(G, node_map)  # relabel nodes so edges match up
        G.add_edges_from(edges)

        # SBR 12/19/17: reset node['id']
        for i in range(len(nodes_dict)):
            nodes_dict[i]['id'] = node_map[nodes_dict[i]['id']]
    else:
        # SBR 12/19/17: id needs to be an int which matches source and target from edges
        # node_map = dict(zip(nodes,range(len(nodes))))  # map to indices for source/target in edges
        # create nodes_dict from graph
        nodes_dict = []
        node_counter = -1
        for node in list(G.nodes(data=True)):
            node_counter += 1
            # if 'id' not in node[1]: # ensure id is in node dict
            node[1]['id'] = node_counter
            nodes_dict.append(node[1])

        # create edges_dict from graph
        nodes = G.nodes()
        node_map = dict(zip(nodes, range(len(nodes))))  # relabel ids so they match the edges

        # relabel nodes in G
        G = nx.relabel_nodes(G, node_map)

        # add node name as node attribute
        nx.set_node_attributes(G, 'node_name', dict(
            zip(range(len(nodes)), [str(n) for n in nodes])
        ))  # make sure node names are strings

        if G.is_multigraph():
            edges_no_data = G.edges(keys=True)
        else:
            edges_no_data = G.edges()

        edges_dict = []

        # SBR 01/22/18: update this for consistency with node id naming convention
        for i in range(len(edges_no_data)):
            if G.is_multigraph():
                source, target, key = edges_no_data[i]
                edges_dict.append(
                    {"source": source, "target": target, "key": key}
                )
            else:
                source, target = edges_no_data[i]
                edges_dict.append(
                    {"source": source, "target": target}
                )

        #        for edge in list(G.edges(data=True)):
        #            if 'source' not in edge[2]: # ensure source is in edge dict
        #                edge[2]['source'] = edge[0]
        #            if 'target' not in edge[2]: # ensure target is in edge dict
        #                edge[2]['target'] = edge[1]
        #            edges_dict.append(edge[2])

        nodes = [node['id'] for node in nodes_dict]  # nodes_dict must contain id

        if G.is_multigraph():
            edges = [(edge['source'], edge['target'], edge['key']) for edge in
                     edges_dict]  # edges_dict must contain source and target
        else:
            edges = [(edge['source'], edge['target']) for edge in
                     edges_dict]  # edges_dict must contain source and target

    # iterate over nodes dict and add attributes to graph
    for attribute in nodes_dict[0].keys():  # under the assumption that all nodes have the same attributes!!!!

        if attribute == 'x':
            xpos = {node['id']: node['x'] for node in nodes_dict}
            nx.set_node_attributes(G, name='xpos', values=xpos)
        elif attribute == 'y':
            ypos = {node['id']: node['y'] for node in nodes_dict}
            nx.set_node_attributes(G, name='ypos', values=ypos)
        elif attribute == 'border_width':
            border_width = {node['id']: node['border_width'] for node in nodes_dict}
            nx.set_node_attributes(G, name='nodeOutline', values=border_width)
        elif attribute == 'title':
            node_titles = {node['id']: node['title'] for node in nodes_dict}
            nx.set_node_attributes(G, name='nodeTitle', values=node_titles)
        elif attribute == 'id':
            node_id = {node['id']: str(node['id']) for node in nodes_dict}
            nx.set_node_attributes(G, name='id', values=node_id)
        else:
            node_att = {node['id']: node[attribute] for node in nodes_dict}
            nx.set_node_attributes(G, name=attribute, values=node_att)

    # SBR 1/22/18: this part doesn't seem to be needed..?
    #    if 'name' not in nodes_dict[0].keys():
    #        print(node_map_r)
    #        print(type(node_map_r[0]))
    #        print(nodes_dict[0]['id'])
    #
    #        node_name = {node_map[node['id']]:str(node_map[node['id']]) for node in nodes_dict}
    #        print(node_name)
    #        nx.set_node_attributes(G, name = 'name', values = node_name)

    # set source and target attributes based on node id's
    sources = [str(edge['source']) for edge in edges_dict]  # assuming edges_dict has a source attribute
    targets = [str(edge['target']) for edge in edges_dict]  # assuming edges_dict has a target attribute
    edge_to_source = dict(zip(edges, sources))
    edge_to_target = dict(zip(edges, targets))
    nx.set_edge_attributes(G, name='source', values=edge_to_source)
    nx.set_edge_attributes(G, name='target', values=edge_to_target)

    for attribute in edges_dict[0].keys():
        if attribute == 'source':
            l = 0  # do nothing
        elif attribute == 'target':
            k = 0  # do nothing
        else:
            if G.is_multigraph():
                edge_att = {(edge['source'], edge['target'], edge['key']): edge[attribute] for edge in edges_dict}
            else:
                edge_att = {(edge['source'], edge['target']): edge[attribute] for edge in edges_dict}
            nx.set_edge_attributes(G, name=attribute, values=edge_att)

            # begin writing the json-style file
    to_string = '{\"elements\":{\"nodes\":['

    # write node data
    for i in range(len(G.nodes())):
        to_string += str('{\"data\":')
        to_string += str(list(dict(G.nodes(data=True)).values())[i])
        if (i == len(G.nodes()) - 1):
            to_string += str('}],\"edges\":[')
        else:
            to_string += str('},')

    # write edges data
    for j in range(len(G.edges())):
        to_string += str('{\"data\":')
        to_string += str(list(G.edges(data=True))[j][2])  # 2 correspondes to the edge attributes
        if j == len(G.edges()) - 1:
            to_string += str('}]},\"data\": {}}')
        else:
            to_string += str('},')

    to_string = to_string.replace('\'', '\"')

    file_str = export_file.split(".")
    f = open((file_str[0] + '.json'), 'w')  # ensure has json ending
    f.write(to_string)
    f.close()


def check_nodes_dict(nodes_dict):
    """
    - Check nodes_dict to make sure it has some required fields.
    - Fill in default values if it is missing them
    - Return updated nodes_dict
    """

    node_keys = nodes_dict[0].keys()
    if 'node_shape' not in node_keys:
        for i in range(len(nodes_dict)):
            nodes_dict[i]['node_shape'] = 'dot'
    if 'color' not in node_keys:
        for i in range(len(nodes_dict)):
            nodes_dict[i]['color'] = '#8BA8D3'
    if 'border_width' not in node_keys:
        for i in range(len(nodes_dict)):
            nodes_dict[i]['border_width'] = 0
    if 'title' not in node_keys:
        for i in range(len(nodes_dict)):
            nodes_dict[i]['title'] = nodes_dict[i]['id']
    if 'degree' not in node_keys:
        for i in range(len(nodes_dict)):
            nodes_dict[i]['degree'] = 3.0

    return nodes_dict


# switch bool from python to JS
def stringify_bool(var):
    return 'true' if var else 'false'
