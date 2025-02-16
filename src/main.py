import click
from rich.console import Console
from .commands import project_commands,config_commands


console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Timectl - A worklog for devs"""
    pass


@cli.group()
def get():
    """Create resources"""
    pass

@cli.group()
def create():
    """Create resources"""
    pass

@cli.group()
def config():
    """Manage Config Files"""
    pass


# Register commands

# Get commands
get.add_command(project_commands.get_projects)

# Project commands
cli.add_command(project_commands.project)
create.add_command(project_commands.create_project)

# Config commands
config.add_command(config_commands.set_config)
config.add_command(config_commands.unset_config)
config.add_command(config_commands.view_config)
config.add_command(config_commands.init_config)


if __name__ == '__main__':
    cli()
