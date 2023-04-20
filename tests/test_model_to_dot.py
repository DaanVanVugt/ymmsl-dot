"""Test plotting of our sample files."""
from ymmsl_dot.main import _load_ymmsl_files
from ymmsl_dot.model_to_dot import plot_model_graph


def test_macro_micro():
    """Test that we can generate dot syntax for
      a macro-micro example without explicit ports."""
    partial_config = _load_ymmsl_files(["docs/examples/macro_micro.ymmsl"])

    graph = plot_model_graph(
        partial_config,
        simplify_edge_labels=True,
        draw_ports=False,
        simple_edges=True,
        show_legend=False,
    )

    str(graph)  # converts to dot and should not error


def test_plot_macro_micro():
    """Test that we can generate a png for
      a macro-micro example without explicit ports."""
    partial_config = _load_ymmsl_files(["docs/examples/macro_micro.ymmsl"])

    graph = plot_model_graph(
        partial_config,
        simplify_edge_labels=True,
        draw_ports=False,
        simple_edges=True,
        show_legend=False,
    )

    graph.create(
        format="svg"
    )  # creates an svg and returns it as a string. Should not crash.
