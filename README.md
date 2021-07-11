# Python project templates using poetry

This repository contains project templates for python. All templates use [poetry](https://python-poetry.org/).

## Requirements

- Python 3.8+ 
- [Poetry](https://python-poetry.org/docs/)
- [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) 

I highly recommend installing [pyenv](https://github.com/pyenv/pyenv) to manage different python versions.

It's also a good idea to have poetry create virtual environments in the project root. To do this, execute:

```shell
poetry config virtualenvs.in-project true
```

## Setting up a new project

To start a new project with the `base` project template, execute:

```shell
cookiecutter -c base https://github.com/JasperHG90/python-project-templates
```

### Setting up poetry

Navigate into your project directory, then execute:

```shell
make install-dependencies
```

Set up a new git repository and configure the pre-commit hooks as follows:

```shell
git init && make setup-pre-commit
```

### Other templates

Currently, there are two available templates:

1. the [base template](https://github.com/JasperHG90/python-project-templates)
   
    ```shell
    cookiecutter -c base https://github.com/JasperHG90/python-project-templates
    ```


2. the [data science template](https://github.com/JasperHG90/python-project-templates/datascience) that is based on the
[cookiecutter data science template](https://github.com/drivendata/cookiecutter-data-science)

    ```shell
    cookiecutter -c datascience https://github.com/JasperHG90/python-project-templates
    ```