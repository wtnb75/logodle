import os
import sys
import click
import matplotlib as mpl
import matplotlib.pyplot as plt
from ._version import VERSION


@click.group(invoke_without_command=True)
@click.version_option(VERSION)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


def init_axes(ax: plt.Axes):
    ax.xaxis.set_major_locator(mpl.ticker.NullLocator())
    ax.yaxis.set_major_locator(mpl.ticker.NullLocator())
    ax.set(xlim=(-1, 1), ylim=(-1, 1))


def set_text(ax: plt.Axes, ch: str, style: str = 'gray', fontname: str = "Sans"):
    ax.set(facecolor=style)
    ax.text(0, 0, ch, horizontalalignment='center',
            verticalalignment='center', fontsize=32, fontweight='bold', color='white',
            fontname=fontname)


@cli.command()
@click.option("--input", "ifp", type=click.File('r'), default=sys.stdin)
@click.option("--output", type=click.Path(dir_okay=False, file_okay=True, writable=True))
@click.option("--fontname", type=str, default="Sans", show_default=True)
@click.option("--upper/--no-upper", default=True, show_default=True)
def create_logo(ifp, output, upper, fontname):
    lines = [x.strip() for x in ifp.readlines()]
    if upper:
        lines = [x.upper() for x in lines]
    width = max([len(x) for x in lines])
    lines = [x.ljust(width) for x in lines]
    height = len(lines)
    answer = lines[-1]
    print("lines", lines, width, height)
    fig, axes = plt.subplots(height, width, figsize=(width, height))
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if answer[x] == c:
                style = '#6aaa64'
            elif c in answer:
                style = '#c9b458'
            else:
                style = '#787c7e'
            init_axes(axes[y, x])
            set_text(axes[y, x], c, style=style, fontname=fontname)
    if output:
        fig.savefig(output)
    else:
        fig.show()
        input("press enter: ")


@cli.command()
def list_fonts():
    import matplotlib.font_manager
    fonts = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
    for i in sorted(fonts):
        click.echo(i)


if __name__ == "__main__":
    cli()
