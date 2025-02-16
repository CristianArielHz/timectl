# cli/commands/config_commands.py
import click
import json
import os
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

console = Console()

CONFIG_FILE = os.path.expanduser("~/.timectl/config.json")

def load_config():
    """Load configuration from JSON file"""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        return {"projects": {}, "settings": {}}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    """Save configuration to JSON file"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

@click.group(name="config")
def config():
    """Configuration management commands"""
    pass

@config.command(name="view")
@click.option("--format", type=click.Choice(['table', 'json'], case_sensitive=False), default='table')
def view_config(format):
    """View current configuration"""
    config = load_config()
    
    if format == 'json':
        # Show formatted JSON
        json_str = json.dumps(config, indent=2)
        syntax = Syntax(json_str, "json", theme="monokai")
        console.print(syntax)
    else:
        # Show as table
        table = Table(title="Configuration")
        table.add_column("Section", style="cyan")
        table.add_column("Key", style="magenta")
        table.add_column("Value", style="green")
        
        # Add project configurations
        for project, project_config in config.get("projects", {}).items():
            for key, value in project_config.items():
                table.add_row("projects", f"{project}.{key}", str(value))
        
        # Add general settings
        for key, value in config.get("settings", {}).items():
            table.add_row("settings", key, str(value))
        
        console.print(table)

@config.command(name="set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Set a configuration value"""
    config = load_config()
    
    # Handle nested keys (e.g., "projects.myproject.description")
    keys = key.split(".")
    
    # Convert string values to appropriate types
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.isdigit():
        value = int(value)
    elif value.replace(".", "").isdigit():
        value = float(value)
    
    # Navigate through nested dictionary
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]
    
    # Set the value
    current[keys[-1]] = value
    save_config(config)
    console.print(f"[green]Configuration updated: {key} = {value}[/green]")

@config.command(name="unset")
@click.argument("key")
def unset_config(key):
    """Remove a configuration value"""
    config = load_config()
    
    # Handle nested keys
    keys = key.split(".")
    
    # Navigate through nested dictionary
    current = config
    for k in keys[:-1]:
        if k not in current:
            console.print(f"[yellow]Key not found: {key}[/yellow]")
            return
        current = current[k]
    
    # Remove the key if it exists
    if keys[-1] in current:
        del current[keys[-1]]
        save_config(config)
        console.print(f"[green]Removed configuration: {key}[/green]")
    else:
        console.print(f"[yellow]Key not found: {key}[/yellow]")

@config.command(name="init")
def init_config():
    """Initialize default configuration"""
    default_config = {
        "projects": {},
        "settings": {
            "default_project": None,
            "date_format": "%Y-%m-%d",
            "time_format": "%H:%M:%S",
            "auto_pause": True,
            "workday_hours": 8
        }
    }
    
    if os.path.exists(CONFIG_FILE):
        confirm = click.confirm("Configuration file already exists. Do you want to reset to defaults?")
        if not confirm:
            return
    
    save_config(default_config)
    console.print("[green]Configuration initialized with default values[/green]")

