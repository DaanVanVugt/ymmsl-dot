import logging
from typing import List, Union

import pydot
from ymmsl.component import Component, Operator
from ymmsl.configuration import PartialConfiguration
from ymmsl.identity import Reference


COLORS = {
    Operator.F_INIT: "#2998ba",
    Operator.O_I: "#eddea1",
    Operator.S: "#f1c40f",
    Operator.O_F: "#e67e22",
}


def port_operator(port: Reference, component: Union[Component, None]):
    """Look up the operator corresponding to a specific port"""
    return (
        component.ports.operator(port)
        if component and component.ports
        else Operator.NONE
    )


def port_shape(operator: str, simple: bool = True):
    """Given a port reference, find the component referred to,
    look up the port type matching this name
    and look up the shape corresponding to the port type."""

    if simple:
        if operator == Operator.F_INIT or operator == Operator.S:
            return "normal"
        return "none"
    else:
        # I think it is quite easy to misinterpret the direction of a MMSL diagram
        # given that the 'weight' of the edge is towards the filled shape.
        # I would consider making the sending_port smaller, but cannot find the setting
        # in graphviz
        # https://www.graphviz.org/docs/attr-types/arrowType/
        OPERATOR_SHAPES = {
            Operator.NONE: "none",
            Operator.F_INIT: "odiamond",
            Operator.O_I: "dot",
            Operator.S: "odot",
            Operator.O_F: "diamond",
        }
        return OPERATOR_SHAPES[operator]


def find_component(name: Reference, components: List[Component]):
    """Find a component by reference"""
    return next(
        (component for component in components if component.name == str(name)), None
    )


def set_style(graph, draw_ports: bool = False):
    """set default properties to make for a more readable DOT file"""
    graph.add_node(
        pydot.Node(
            "node",
            shape="plain" if draw_ports else "box",
            style="rounded",
            fixedsize="false",
            width=2,
            penwidth=2,
            height=1,
            labelloc="c",
        )
    )

    # set default edge properties
    graph.add_node(
        pydot.Node(
            "edge",
            dir="both",
            labelfontsize=10,
            fontsize=10,
            penwidth=2,
            len=2,
        )
    )


def trim_sending_port(identifier: str):
    """Strip _out suffix from identifier"""
    return identifier[:-4] if identifier.endswith("_out") else identifier


def trim_receiving_port(identifier: str):
    """Strip _in, _init suffix from identifier"""
    if identifier.endswith("_in"):
        return identifier[:-3]
    if identifier.endswith("_init"):
        return identifier[:-5]
    return identifier


def headport(identifier: Reference, component: Union[Component, None]):
    """Given a reference, return the portPos.
    https://www.graphviz.org/docs/attr-types/portPos/
    """
    return str(identifier)


def tailport(identifier: Reference, component: Union[Component, None]):
    """Given a reference, return the portPos.
    https://www.graphviz.org/docs/attr-types/portPos/
    """
    return str(identifier)


def port_shortname(identifier: Reference):
    """Strip suffixes and summarize names to only a few characters"""
    identifier = trim_sending_port(trim_receiving_port(str(identifier)))
    return "".join([s[0] for s in identifier.split("_")]).upper()


def legend_html_label():
    return f"""<<TABLE CELLSPACING="0" CELLBORDER="0" >
  <TR>
    <TD BGCOLOR='{COLORS[Operator.F_INIT]}'>F_INIT</TD>
    <TD BGCOLOR='{COLORS[Operator.O_I]}'>O_I</TD>
    <TD><B>legend</B></TD>
    <TD BGCOLOR='{COLORS[Operator.S]}'>S</TD>
    <TD BGCOLOR='{COLORS[Operator.O_F]}'>O_F</TD>
  </TR>
</TABLE>>"""
    pass


def component_html_label(component: Component):
    """Construct a HTML-like label (https://graphviz.org/doc/info/shapes.html#html)"""

    if component.ports is None:
        logging.warning("no ports defined on component, skipping.")
        return component.name

    label = "<<TABLE CELLSPACING='0' CELLBORDER='0' >\n  <TR>\n"

    for port in sorted(component.ports.f_init):
        label += f"    <TD PORT='{port}' BGCOLOR='{COLORS[Operator.F_INIT]}'\
            >{port_shortname(port)}</TD>\n"
    if len(component.ports.f_init) == 0:
        label += f"    <TD BGCOLOR='{COLORS[Operator.F_INIT]}'></TD>\n"
    for port in sorted(component.ports.o_i):
        label += f"    <TD PORT='{port}' BGCOLOR='{COLORS[Operator.O_I]}'\
            >{port_shortname(port)}</TD>\n"
    if len(component.ports.o_i) == 0:
        label += f"    <TD BGCOLOR='{COLORS[Operator.O_I]}'></TD>\n"

    label += f"    <TD><B>{component.name}</B></TD>\n"

    for port in sorted(component.ports.s):
        label += f"    <TD PORT='{port}' BGCOLOR='{COLORS[Operator.S]}'\
            >{port_shortname(port)}</TD>\n"
    if len(component.ports.s) == 0:
        label += f"    <TD BGCOLOR='{COLORS[Operator.S]}'></TD>\n"
    for port in sorted(component.ports.o_f):
        label += f"    <TD PORT='{port}' BGCOLOR='{COLORS[Operator.O_F]}'\
            >{port_shortname(port)}</TD>\n"
    if len(component.ports.o_f) == 0:
        label += f"    <TD BGCOLOR='{COLORS[Operator.O_F]}'></TD>\n"

    return label.replace("'", '"') + "</TR></TABLE>>"


def plot_model_graph(
    config: PartialConfiguration,
    simplify_edge_labels: bool = True,
    draw_ports: bool = False,
    simple_edges: bool = True,
    show_legend: bool = True,
    edge_labels: bool = False,
) -> None:
    """Convert a PartialConfiguration into DOT format."""
    graph = pydot.Dot(
        config.model.name,
        graph_type="digraph",
        layout="dot",
        pad=1,
        # splines="ortho",
        nodesep=0.6,
        ranksep=0.75,
        fontname="Sans-Serif",
    )
    # be very careful with ortho splines, I have seen it put edges
    # upside down and eating labels
    set_style(graph, draw_ports=draw_ports)

    if draw_ports:
        label_method = component_html_label
    else:
        def label_method(x):
            return x.name

    # Start with a legend node
    if draw_ports and show_legend:
        graph.add_node(pydot.Node("legend", label=legend_html_label()))

    for component in config.model.components:
        graph.add_node(pydot.Node(str(component.name), label=label_method(component)))

    # assume that conduits are ordered by port
    last_port = None
    for conduit in config.model.conduits:
        # emit an edge[sametail=] config for this port name
        # if it is changed from the previous one
        # note that this does not work for self-loops:
        # https://gitlab.com/graphviz/graphviz/-/blob/main/lib/dotgen/sameport.c#L53
        # the sametail attribute does not work with explicit ports, skip it
        if str(conduit.sending_port()) != last_port and not draw_ports:
            graph.add_node(pydot.Node("edge", sametail=str(conduit.sending_port())))
            last_port = str(conduit.sending_port())

        # can we do this more elegantly?
        sender = find_component(conduit.sending_component(), config.model.components)
        receiver = find_component(
            conduit.receiving_component(), config.model.components
        )

        # Due to yMMSL conventions we cannot have edges with the same head (since
        # an input port can only have one conduit connected to it)
        port_config = {
            "tailport": tailport(conduit.sending_port(), sender),
            "headport": headport(conduit.receiving_port(), receiver),
        }

        edge = pydot.Edge(
            str(conduit.sending_component()),
            str(conduit.receiving_component()),
            arrowtail=port_shape(
                port_operator(
                    conduit.sending_port(),
                    sender,
                ),
                simple_edges,
            ),
            arrowhead=port_shape(
                port_operator(
                    conduit.receiving_port(),
                    receiver,
                ),
                simple_edges,
            ),
            **port_config,
        )

        # if port names match exactly (optionally when removing an _in or _out suffix)
        # we show the name on the conduit instead of on the port
        port_names_match = trim_sending_port(
            str(conduit.sending_port())
        ) == trim_receiving_port(str(conduit.receiving_port()))

        if port_names_match and simplify_edge_labels:
            if edge_labels:
                edge.set_label(trim_sending_port(str(conduit.sending_port())))
        else:
            edge.set_taillabel(str(conduit.sending_port()))
            edge.set_headlabel(str(conduit.receiving_port()))

        # we could consider setting a minlen based on the text length and font size
        graph.add_edge(edge)

    return graph
