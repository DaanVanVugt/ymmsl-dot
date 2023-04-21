[![CI](https://github.com/DaanVanVugt/ymmsl-dot/workflows/ci/badge.svg?branch=main)](https://github.com/DaanVanVugt/ymmsl-dot/actions?workflow=ci)

[![Codecov](https://codecov.io/gh/DaanVanVugt/ymmsl-dot/branch/main/graph/badge.svg)](https://codecov.io/gh/DaanVanVugt/ymmsl-dot)

<!--[![Read the Docs](https://img.shields.io/readthedocs/ymmsl-dot/latest?label=Read%20the%20Docs)](https://ymmsl-dot.readthedocs.io/en/latest/index.html) -->

# yMMSL plotting tool

A tool to visualise yMMSL files using `graphviz` and `ymmsl-python`.

# Examples
Two examples are shown here, a simple one [macro_micro](./docs/examples/macro_micro.ymmsl), and a more complex one [complex](./docs/examples/complex.ymmsl).

## Default
![Default options](./docs/static/complex.svg)

## Explicit ports, simple arrows, legend (`-p -s -l`)
![More options](./docs/static/complex_spl.svg)


# Usage

    Usage: ymmsl graph [OPTIONS] YMMSL_FILES...

      Plot a graphical representation of the passed yMMSL files.

      To help develop or understand about a coupled simulation it may be useful to
      view a graphical representation.

      If multiple yMMSL files are given, then they will be combined left to right,
      i.e. if there are conflicting declarations, the one from the file last given
      is used.

      Result:

        A graph is displayed or saved to disk, containing all the defined
        components and the connections between them.

      Examples:

        ymmsl graph simulation.ymmsl

    Options:
      -o, --out FILE                  Output file (default ./output.format)
      -f, --fmt [canon|cmap|cmapx|cmapx_np|dia|dot|fig|gd|gd2|gif|hpgl|imap|imap_np|ismap|jpe|jpeg|jpg|mif|mp|pcl|pdf|pic|plain|plain-ext|png|ps|ps2|svg|svgz|vml|vmlz|vrml|vtx|wbmp|xdot|xlib]
                                      Set output format (default svg).
      -w, --viewer TEXT               Open with specified viewer (try xdg-open)
      -v, --verbose                   Show more info (prints the generated dot
                                      syntax)
      -p, --ports                     Explicitly draw component ports.
      -l, --legend                    Show a legend (only with --ports).
      -s, --simple-edges              Only indicate conduit direction, not port
                                      types.
      --portlabels                    Never simplify matching port labels along an
                                      edge.
      --help                          Show this message and exit.

# Issues and Discussions

As usual for any GitHub-based project, raise an
[issue](https://github.com/DaanVanVugt/ymmsl-dot/issues) if you find any
bug or want to suggest an improvement, or open a
[discussion](https://github.com/DaanVanVugt/ymmsl-dot/discussions) if
you want to discuss.

# Generated documentation

There is a `docs/` folder containing sphinx documentation, but this has not yet been filled completely.
Build it with
```bash
sphinx-build docs html
```