import pytest
import os
import json
from click.testing import CliRunner
from src.main import cli
from src.commands.config_commands import config
from unittest.mock import MagicMock


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


def test_create_issue(runner, temp_config):
    result = runner.invoke(config, ['init'])

    # Create initial project
    runner.invoke(cli, ['create', 'project', 'test'])

    # Create an issue
    result = runner.invoke(cli, ['create', 'issue', '-n', 'login', '-p', 'test'])
    assert result.exit_code == 0
    assert 'Issue login created in project test'


@pytest.fixture
# Mocked configuration data to simulate a project with no issues
def mock_config():
    return {
        "projects": {
            "test_project": {
                "issues": []
            }
        }
    }


def test_create_issue_success(mock_config, mocker):
    # Mock the load_config and save_config functions
    mocker.patch('src.commands.project_commands.load_config', return_value=mock_config)
    save_config_mock = MagicMock()
    mocker.patch('src.commands.project_commands.save_config', save_config_mock)

    runner = CliRunner()

    # Run the Click command using CliRunner
    result = runner.invoke(cli, ['create', 'issue', '-p',
                                 'test_project', '-n', 'New Issue'])

    # Ensure the result was successful
    assert result.exit_code == 0
    assert 'Issue New Issue created in project test_project' in result.output

    # Verify that the issue was added to the mock_config
    assert len(mock_config["projects"]["test_project"]["issues"]) == 1
    assert mock_config["projects"]["test_project"]["issues"][0]["name"] == "New Issue"
    assert "time_entries" in mock_config["projects"]["test_project"]["issues"][0]
    assert "created_at" in mock_config["projects"]["test_project"]["issues"][0]

    # Verify that save_config was called with the updated config
    save_config_mock.assert_called_once()
    updated_config = save_config_mock.call_args[0][0]

    # Ensure that the save_config was called with the updated mock_config
    assert len(updated_config["projects"]["test_project"]["issues"]) == 1
    first_issue = updated_config["projects"]["test_project"]["issues"][0]
    assert first_issue["name"] == "New Issue"
    assert "time_entries" in updated_config["projects"]["test_project"]["issues"][0]
    assert "created_at" in updated_config["projects"]["test_project"]["issues"][0]


def test_create_issue_project_not_found(mock_config, mocker):
    # Mock the load_config to simulate no existing project
    mocker.patch('src.commands.project_commands.load_config',
                 return_value={"projects": {}})

    runner = CliRunner()

    # Run the Click command using CliRunner
    result = runner.invoke(cli, ['create', 'issue', '-p',
                                 'non_existing_project', '-n', 'New Issue'])

    # Ensure the result was successful
    assert result.exit_code == 0
    assert 'Project non_existing_project does not exist yet!' in result.output
