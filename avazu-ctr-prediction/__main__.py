"""Entry point for avazu-ctr-prediction library."""
import click
from loguru import logger

@click.group()
def cli():
    """Run the main function of the package. (Add more description here...)

    To start using it run a command like:

    "avazu-ctr-prediction bau --option1=test_option --debug"
    """
    pass


@cli.command(name="bau")
@click.option(
    "--option1",
    default=str,
    required=False,
    help=f"TODO: Explain what the argument passed here to the main function does. Do not forget to tell what happensif left empty (if left empty it will do ...)",
)
@click.option("--save/--do-not-save", default=False)
@click.option("--debug/--no-debug", default=False)
def cmd_bau(option1: str, save: bool, debug: bool):
    """Do XYZ."""
    bau(option1, save, debug=debug)