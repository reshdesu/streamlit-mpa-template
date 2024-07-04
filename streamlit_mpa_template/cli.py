import click
from loguru import logger

logger.enable(__package__)


@click.command()
def build_run_app():
    """Run the app via cli"""
    from streamlit_mpa_template.build import build_helper

    bh = build_helper.BuildHelper()
    bh.run_container()
