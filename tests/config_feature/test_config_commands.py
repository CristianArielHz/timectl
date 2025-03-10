# test/project_feature/test_config_commands.py
import pytest
import os
from click.testing import CliRunner
from src.commands.config_commands import config, load_config


@pytest.fixture
def runner():
    return CliRunner(mix_stderr=False)  # Allow stderr capture


@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config file"""
    original_home = os.environ.get("HOME")  # Save the original HOME
    os.environ["HOME"] = str(tmp_path)  # Temporarily change home directory

    # Define the path for the config file relative to HOME
    temp_config_file = tmp_path / ".timectl" / "config.json"
    os.makedirs(os.path.dirname(temp_config_file), exist_ok=True)
    yield str(temp_config_file)  # Yield the temporary config file path

    # Cleanup
    if os.path.exists(temp_config_file):
        os.remove(temp_config_file)
    os.environ["HOME"] = original_home  # Restore the original HOME


def test_init_config(runner, temp_config):
    """Test configuration initialization"""
    result = runner.invoke(config, ['init'])
    assert result.exit_code == 0
    assert "Configuration initialized with default values" in result.output


def test_set_config(runner, temp_config):
    """Test setting configuration values"""
    # Set a simple value
    result = runner.invoke(config, ['set', 'settings.test_key', 'test_value'])
    assert result.exit_code == 0
    assert "Configuration updated" in result.output

    # Set a nested value
    result = runner.invoke(config, ['set', 'projects.myproject.name', 'My Project'])
    assert result.exit_code == 0

    # Verify values were set correctly
    config_data = load_config()
    assert config_data["settings"]["test_key"] == "test_value"
    assert config_data["projects"]["myproject"]["name"] == "My Project"


def test_view_config(runner, temp_config):
    """Test viewing configuration"""
    # Initialize with some data
    runner.invoke(config, ['init'])
    runner.invoke(config, ['set', 'projects.testproject.name', 'Test Project'])

    # Test table format
    result = runner.invoke(config, ['view'])
    assert result.exit_code == 0
    assert "Test Project" in result.output

    # Test JSON format
    result = runner.invoke(config, ['view', '--format', 'json'])
    assert result.exit_code == 0
    assert "testproject" in result.output


def test_unset_config(runner, temp_config):
    """Test removing configuration values"""
    # Set and then unset a value
    runner.invoke(config, ['set', 'settings.test_key', 'test_value'])
    result = runner.invoke(config, ['unset', 'settings.test_key'])
    assert result.exit_code == 0
    assert "Removed configuration" in result.output

    # Verify it was removed
    config_data = load_config()
    assert "test_key" not in config_data["settings"]


def test_type_conversion(runner, temp_config):
    """Test automatic type conversion of values"""
    tests = [
        ('settings.integer', '42', int),
        ('settings.float', '3.14', float),
        ('settings.boolean', 'true', bool),
        ('settings.string', 'hello', str)
    ]

    for key, value, expected_type in tests:
        runner.invoke(config, ['set', key, value])
        config_data = load_config()
        keys = key.split('.')
        current = config_data
        for k in keys:
            current = current[k]
        assert isinstance(current, expected_type)
