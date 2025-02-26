# tests/project_feature/test_project_commands.py

import os
import json
import tempfile
import pytest
from click.testing import CliRunner
from src.commands.project_commands import create_project, create_issue, get_projects


@pytest.fixture
def temp_config(tmp_path):
    config = {"projects": {}}
    config_file = tmp_path / "config.json"
    with config_file.open("w") as f:
        json.dump(config, f)
    yield config_file


def test_create_project(temp_config):
    runner = CliRunner()
    result = runner.invoke(create_project, ["TestProject"])
    assert result.exit_code == 0
    assert "Project TestProject created successfully" in result.output


def test_create_issue_nonexistent_project(temp_config):
    runner = CliRunner()
    result = runner.invoke(
        create_issue, ["--project", "Nonexistent", "--name", "Issue1"]
    )
    assert result.exit_code == 0
    assert "Project Nonexistent does not exist yet" in result.output


def test_get_projects_no_projects(temp_config):
    runner = CliRunner()
    result = runner.invoke(get_projects)
    assert result.exit_code == 0
    assert "No projects found" in result.output


def test_create_issue(temp_config):
    runner = CliRunner()
    # First, create a project.
    runner.invoke(create_project, ["TestProject"])
    # Then, create an issue within that project.
    result = runner.invoke(
        create_issue, ["--project", "TestProject", "--name", "Issue1"]
    )
    assert result.exit_code == 0
    assert (
        "Issue Issue1 created in project TestProject" in result.output
    )
