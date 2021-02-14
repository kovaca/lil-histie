import io
import json
import sys
from math import floor
import click

CHARS = {
    "fill_1": "▁",
    "fill_2": "▂",
    "fill_3": "▃",
    "fill_4": "▄",
    "fill_5": "▅",
    "fill_6": "▆",
    "fill_7": "▇",
    "fill_8": "█",
    "fill": "█",
}

def draw_hist(normed_hist_list, shape, height, bins):
    """ takes a list of histogram , shape, height, and bin count """

    # TODO make the offset configurable
    y_offset = " "
    y_label = " "

    # click.echo("")
    # Build plot from top level
    for depth in range(height - 1, -1, -1):

        # Draw Y axis
        if depth == height / 2:
            sys.stdout.write(y_label + "│")
        else:
            sys.stdout.write(y_offset + "│")

        # Draw bars. Surely there is a more elegant approach. Alas.
        for item in normed_hist_list:
            floored_item = floor(item)
            if floored_item >= depth:
                if floored_item == depth and item % 1 < 0.1875 and item % 1 > 0.0625:
                    sys.stdout.write(CHARS["fill_1"])
                elif floored_item == depth and item % 1 < 0.3125 and item % 1 > 0.1875:
                    sys.stdout.write(CHARS["fill_2"])
                elif floored_item == depth and item % 1 < 0.4375 and item % 1 > 0.3125:
                    sys.stdout.write(CHARS["fill_3"])
                elif floored_item == depth and item % 1 < 0.5625 and item % 1 > 0.4375:
                    sys.stdout.write(CHARS["fill_4"])
                elif floored_item == depth and item % 1 < 0.6875 and item % 1 > 0.5625:
                    sys.stdout.write(CHARS["fill_5"])
                elif floored_item == depth and item % 1 < 0.8125 and item % 1 > 0.6875:
                    sys.stdout.write(CHARS["fill_6"])
                elif floored_item == depth and item % 1 < 0.9375 and item % 1 > 0.8125:
                    sys.stdout.write(CHARS["fill_7"])
                elif floored_item == depth and item % 1 > 0.9375:
                    sys.stdout.write(CHARS["fill_8"])
                elif floored_item > depth:
                    sys.stdout.write(CHARS["fill"])
                else:
                    sys.stdout.write(" ")
                continue
            else:
                sys.stdout.write(" ")
        click.echo("")

    # Draw X axis
    click.echo(y_offset + "└" + "─" * (bins))
    click.echo(f"{y_offset} {shape[0]:<12.4g}{shape[1]:>{bins-12}.4g}")

@click.command()
@click.option(
    "--height",
    "-h",
    default=10,  # type=int,
    type=click.IntRange(1, 50),
    help="The height of the chart in lines.",
)
def cli(height):
    """Creates a little histi gram if piped from `gdalinfo -hist -json` output."""
    term_width, _term_height = click.get_terminal_size()
    stdin_wrapper = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8-sig")
    try:
        n = json.load(stdin_wrapper)
    except Exception:
        click.echo(
            "Oops! Something went wrong. Was the input json? Was the -hist created?"
        )
        click.echo(sys.stderr)
        sys.exit(1)
    for b in range(len(n["bands"])):
        click.echo(f"Band: {n['bands'][b]['band']}")
        buckets = n["bands"][b]["histogram"]["buckets"]
        bins = len(buckets)
        while bins > (term_width - 1):
            buckets = [i + k for i, k in zip(buckets[0::2], buckets[1::2])]
            bins = len(buckets)
        max_count = max(buckets)
        shape = (n["bands"][b]["histogram"]["min"], n["bands"][b]["histogram"]["max"])
        normed_hist_list = [float(x) * height / max_count for x in buckets]
        draw_hist(normed_hist_list, shape, height, bins)
