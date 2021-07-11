import tempfile
import pathlib
from cookiecutter.main import cookiecutter
import pytest
import toml
import yaml


@pytest.fixture(scope="class")
def cookiecutter_setup(request):
    request.cls.template_dir = str(pathlib.Path(__file__).parent.parent)
    request.cls.args = {
        "project_name": "cookiecutter-test",
        "repo_name": "cookiecutter-poetry-env",
        "module_name": "mypythoncode",
        "author_name": "walter",
        "author_email": "walter@security.com",
        "description": "mydescription",
        "github_url": "myrepo/mycompany",
        "open_source_license": "MIT",
        "cloud_vendor": "GCP",
        "data_bucket": "mybucket",
        "project_profile_or_id": "mygcpproject",
    }
    request.cls.dev_dependencies = {
        "black": "^20.8b1",
        "flake8": "^3.9.2",
        "mypy": "^0.812",
        "pre-commit": "^2.12.1",
        "pytest": "^5.2",
        "pytest-cov": "^2.11.1",
        "pytest-dotenv": "^0.5.2",
        "bump2version": "^1.0.1",
        "isort": "^5.9.2"
    }
    request.cls.python_version = ">=3.8,<3.10"
    request.cls.circleci_docker_python = "cimg/python:3.8"
    module_name = request.cls.args.get("module_name")
    with tempfile.TemporaryDirectory() as tmpdir:
        cookiecutter(
            template=request.cls.template_dir,
            output_dir=tmpdir,
            no_input=True,
            extra_context=request.cls.args,
        )
        cookiecutter_file_path = pathlib.Path(tmpdir) / "cookiecutter-poetry-env"
        # Sort files because it may be different in CI/CD pipeline because of different OS
        request.cls.cookiecutter_files = sorted(
            [str(f).split("/")[-1] for f in cookiecutter_file_path.glob("*")]
        )
        request.cls.pyproject = toml.load(
            str(cookiecutter_file_path / "pyproject.toml")
        )
        with (cookiecutter_file_path / ".circleci/config.yml").open("r") as infile:
            request.cls.circleci_config = yaml.safe_load(infile)
        with (cookiecutter_file_path / ".pre-commit-config.yaml").open("r") as infile:
            request.cls.precommit_config = yaml.safe_load(infile)
        request.cls.source_code_is_dir = (
            cookiecutter_file_path / module_name
        ).is_dir()
        request.cls.source_code_dir_content = sorted([
            str(f).split("/")[-1]
            for f in (cookiecutter_file_path / module_name).glob("*")
        ])
        request.cls.tests_is_dir = (cookiecutter_file_path / "tests").is_dir()
