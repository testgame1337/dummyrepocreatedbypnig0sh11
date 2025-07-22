"""
Command-line interface for Vulcan
"""

import click
import sys
from . import __version__
from .core import process_data, analyze_system, run_task


@click.group()
@click.version_option(version=__version__)
def cli():
    """Vulcan - A versatile tool for system operations and data processing."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--format", "-f", type=click.Choice(["json", "yaml", "csv"]), default="json", help="Output format")
def process(input_file, output, format):
    """Process data from input file."""
    try:
        result = process_data(input_file, output_format=format)
        if output:
            with open(output, "w") as f:
                f.write(result)
        else:
            click.echo(result)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--detailed", "-d", is_flag=True, help="Show detailed analysis")
def analyze(detailed):
    """Analyze system information."""
    try:
        result = analyze_system(detailed=detailed)
        click.echo(result)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("task_name")
@click.option("--config", "-c", type=click.Path(exists=True), help="Configuration file")
def run(task_name, config):
    """Run a predefined task."""
    try:
        result = run_task(task_name, config_file=config)
        click.echo(result)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()