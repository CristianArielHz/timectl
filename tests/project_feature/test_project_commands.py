# test/project_feature/test_project_commands.py
import pytest
import os
import json
from click.testing import CliRunner
from src.main import cli
from src.commands.config_commands import config


@pytest.fixture
def runner():
    """Provides a CLI test runner"""
    return CliRunner()


@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config file"""
    original_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)

    # Ensure the .timectl directory exists
    config_dir = tmp_path / ".timectl"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Define path for config file
    temp_config_file = config_dir / "config.json"

    # IMPORTANT: Initialize the config file with empty JSON structure
    with open(temp_config_file, 'w') as f:
        json.dump({"projects": {}}, f)

    global CONFIG_FILE
    CONFIG_FILE = str(temp_config_file)

    yield str(temp_config_file)

    # Cleanup
    if os.path.exists(temp_config_file):
        os.remove(temp_config_file)

    os.environ["HOME"] = original_home


def test_cli_base():
    """Test the base CLI command works"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Timectl - A worklog for devs' in result.output


def test_project_command():
    """Test the project command group exists and works"""
    runner = CliRunner()
    result = runner.invoke(cli, ['project', '--help'])
    assert result.exit_code == 0
    assert 'Project management commands' in result.output


def test_version():
    """Test version command returns correct version"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert '0.1.0' in result.output


# Example of testing with isolated filesystem
def test_with_isolated_fs(runner):
    """Test command that might interact with filesystem"""
    with runner.isolated_filesystem():
        # Here you can create test files and directories
        # that will be cleaned up after the test
        result = runner.invoke(cli, ['project'])
        assert result.exit_code == 0


def test_create_project(runner, temp_config):
    """Test creating a new project"""

    # After running init
    result = runner.invoke(config, ['init'])
    print(f"Init result: {result.exit_code}")
    print(f"Config file exists after init: {os.path.exists(temp_config)}")

    # Test creating a project
    result = runner.invoke(cli, ['create', 'project', 'test'])
    assert result.exit_code == 0
    assert 'Project test created successfully' in result.output


def test_create_duplicate_project(runner, temp_config):
    """Test attempting to create a duplicate project"""

    # After running init
    result = runner.invoke(config, ['init'])
    print(f"Init result: {result.exit_code}")
    print(f"Config file exists after init: {os.path.exists(temp_config)}")

    # Create initial project
    runner.invoke(cli, ['create', 'project', 'test'])

    # Try to create duplicate
    result = runner.invoke(cli, ['create', 'project', 'test'])
    assert result.exit_code == 0
    assert 'Project test already exists!' in result.output
