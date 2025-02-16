# test/project_feature/test_project_commands.py
import pytest
import os
import json
from click.testing import CliRunner
from src.main import cli
from src.commands.project_commands import project
from src.commands.config_commands import config, CONFIG_FILE, load_config

@pytest.fixture
def runner():
    """Provides a CLI test runner"""
    return CliRunner()

@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config file"""
    original_config_file = CONFIG_FILE
    temp_config_file = tmp_path / "config.json"
    print('archivo de prueba',temp_config_file)
    os.environ["HOME"] = str(tmp_path)  # Temporarily change home directory
    yield str(temp_config_file)
    # Cleanup
    if os.path.exists(temp_config_file):
        os.remove(temp_config_file)
    os.environ["HOME"] = original_config_file

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
  
    # Test creating a project
    result = runner.invoke(config, ['init', 'y'])
    
    # Test creating a project
    result = runner.invoke(cli, ['project', 'test'])
    assert result.exit_code == 0
    assert 'Project test created successfully' in result.output

    # Verify project was created in config
    with open(temp_config, 'r') as f:
        config_data = json.load(f)
    assert 'test' in config_data['projects']
    assert config_data['projects']['test']['name'] == 'test'

def test_create_duplicate_project(runner, temp_config):
    """Test attempting to create a duplicate project"""
    # Initialize config first
    runner.invoke(config, ['init'])
    
    # Create initial project
    runner.invoke(cli, ['project', 'test'])
    
    # Try to create duplicate
    result = runner.invoke(cli, ['project', 'test'])
    assert result.exit_code == 0
    assert 'Project test already exists!' in result.output