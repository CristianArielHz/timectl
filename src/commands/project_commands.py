import click
from rich.console import Console
from rich.table import Table
from .config_commands import load_config, save_config
from datetime import datetime
console = Console()


@click.group()
def project():
    """Project management commands"""
    pass


@click.command(name="project")
@click.argument("name")
def create_project(name):
    """Create a new project"""
    config = load_config()
    project_name = name

    if project_name in config["projects"]:
        console.print(f"[red]Project {project_name} already exists![/]")
        return

    config["projects"][project_name] = {
        "name": project_name,
        "created_at": str(datetime.now().isoformat())
    }
    save_config(config)
    console.print(f"[green]Project {name} created successfully[/green]")


@click.command(name="projects")
def get_projects():
    """List all projects"""
    config = load_config()
    if not config["projects"]:
        console.print("[yellow]No projects found.[/]")
        return

    table = Table(box=None)
    table.add_column("Project", style="green")
    table.add_column("Created")

    # Use .items() to get both key and value, and access created_at from project data
    for name, project_data in config["projects"].items():
        table.add_row(name.upper(), project_data["created_at"])

    # Print table once after all rows are added
    console.print(table)
