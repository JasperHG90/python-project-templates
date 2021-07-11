from typing import Union, List, Dict
import pytest


def helper_parse_circleci_command(
    steps: List[Union[str, Dict[str, Union[List, str]]]],
    step_name: str) -> str:
    """Helper function that retrieves the command used for a particular step in a parsed circleci configuration
    Parameters
    ----------
    steps : List[str, Dict[str, Union[List, str]]]
        steps used in a circleci pipeline workflow
    step_name : str
        name of the step for which to extract the command
    Returns
    -------
    str
        the command used for a particular step
    Raises
    ------
    ValueError
        this error is raised when the step isn't found in the workflow
    """
    cmd: Union[str, None] = None
    for step in steps:
        if not isinstance(step, dict):
            continue
        if step.get("run") is None:
            continue
        if not isinstance(step.get("run"), dict):
            continue
        if step.get("run").get("name") == step_name:
            cmd = step.get("run").get("command")
    if cmd is None:
        raise ValueError(f"'{step_name}' command not found in circleci config")
    return cmd


@pytest.mark.usefixtures("cookiecutter_setup")
class TestCircleConfig:
    def test_circleci_docker_version(self):
        assert (
            self.circleci_config.get("jobs").get("build").get("docker")[0].get("image")
            == self.circleci_docker_python
        )

    def test_circleci_cookiecutter_parsed_source_dir(self):
        circleci_steps = self.circleci_config.get("jobs").get("build").get("steps")
        cmd = helper_parse_circleci_command(circleci_steps, "Pytest")
        cmd_split = cmd.split("--cov=")[-1]
        assert cmd_split == self.args.get("module_name")

    def test_circleci_mypy_cmd(self):
        circleci_steps = self.circleci_config.get("jobs").get("build").get("steps")
        cmd = helper_parse_circleci_command(circleci_steps, "Type checks")
        assert cmd == "poetry run mypy --ignore-missing-imports ."

    def test_circleci_black_cmd(self):
        circleci_steps = self.circleci_config.get("jobs").get("build").get("steps")
        cmd = helper_parse_circleci_command(circleci_steps, "Check code formatting")
        assert cmd == "poetry run black --check ."


@pytest.mark.usefixtures("cookiecutter_setup")
class TestCookiecutterTemplate:
    def test_files_present(self):
        assert self.cookiecutter_files == sorted([
            '.circleci',
            '.env',
            '.gitignore',
            '.pre-commit-config.yaml',
            'LICENSE',
            'Makefile',
            'README.md',
            'data', 'docs', 'models', 'mypythoncode',
            'notebooks', 'pyproject.toml',
            'references', 'reports', 'setup.cfg', 'tests'
        ])

    def test_pyproject_poetry_env_name(self):
        assert self.pyproject.get("tool").get("poetry").get("name") == self.args.get("repo_name")

    def test_pyproject_python_version(self):
        assert (
            self.pyproject.get("tool").get("poetry").get("dependencies").get("python")
            == self.python_version
        )

    def test_pyproject_python_dev_dependencies(self):
        assert (
            self.pyproject.get("tool").get("poetry").get("dev-dependencies")
            == self.dev_dependencies
        )

    def test_pyproject_include_packages(self):
        assert (
            self.pyproject.get("tool").get("poetry").get("packages")[0].get("include")
            == self.args.get("module_name")
        )

    def test_source_code_is_dir(self):
        assert self.source_code_is_dir == True

    def test_tests_is_dir(self):
        assert self.tests_is_dir == True


@pytest.mark.usefixtures("cookiecutter_setup")
class TestPrecommitConfig:
    def test_pre_commit_hooks_repo(self):
        assert (
            self.precommit_config.get("repos")[0].get("repo")
            == "https://github.com/pre-commit/pre-commit-hooks"
        )

    def test_pre_commit_hooks_version(self):
        assert self.precommit_config.get("repos")[0].get("rev") == "v3.2.0"

    def test_pre_commit_hooks_ids(self):
        hook_ids = sorted(
            [
                hook.get("id")
                for hook in self.precommit_config.get("repos")[0].get("hooks")
            ]
        )
        assert hook_ids == [
            "check-ast",
            "check-toml",
            "check-yaml",
            "debug-statements",
            "end-of-file-fixer",
            "no-commit-to-branch",
            "trailing-whitespace",
        ]

    def test_pre_commit_black_repo(self):
        assert (
            self.precommit_config.get("repos")[1].get("repo")
            == "https://github.com/psf/black"
        )

    def test_pre_commit_black_version(self):
        assert self.precommit_config.get("repos")[1].get("rev") == "20.8b1"

    def test_pre_commit_black_id(self):
        hook_ids = sorted(
            [
                hook.get("id")
                for hook in self.precommit_config.get("repos")[1].get("hooks")
            ]
        )
        assert hook_ids == ["black"]

    def test_pre_commit_mypy_repo(self):
        assert (
            self.precommit_config.get("repos")[3].get("repo")
            == "https://github.com/pre-commit/mirrors-mypy"
        )

    def test_pre_commit_mypy_version(self):
        assert self.precommit_config.get("repos")[3].get("rev") == "v0.812"

    def test_pre_commit_isort_version(self):
        assert self.precommit_config.get("repos")[4].get("rev") == "5.9.2"

    def test_pre_commit_isort_repo(self):
        assert (
            self.precommit_config.get("repos")[4].get("repo")
            == "https://github.com/pycqa/isort"
        )

    def test_pre_commit_mypy_ids(self):
        hook_ids = sorted(
            [
                hook.get("id")
                for hook in self.precommit_config.get("repos")[3].get("hooks")
            ]
        )
        assert hook_ids == ["mypy"]

    def test_circleci_docker_version(self):
        assert (
            self.circleci_config.get("jobs").get("build").get("docker")[0].get("image")
            == self.circleci_docker_python
        )

    def test_circleci_cookiecutter_parsed_source_dir(self):
        circleci_steps = self.circleci_config.get("jobs").get("build").get("steps")
        cmd = helper_parse_circleci_command(circleci_steps, "Pytest")
        cmd_split = cmd.split("--cov=")[-1]
        assert cmd_split == self.args.get("module_name")

    def test_circleci_mypy_checks_cmd(self):
        circleci_steps = self.circleci_config.get("jobs").get("build").get("steps")
        cmd = helper_parse_circleci_command(circleci_steps, "Type checks")
        assert cmd == "poetry run mypy --ignore-missing-imports ."

    def test_circleci_black_checks_cmd(self):
        circleci_steps = self.circleci_config.get("jobs").get("build").get("steps")
        cmd = helper_parse_circleci_command(circleci_steps, "Check code formatting")
        assert cmd == "poetry run black --check ."
