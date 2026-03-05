# nomad-plugins-metadata

Canonical metadata schema and tooling foundation for the NOMAD plugin registry ecosystem.

## Phase 1 status

Phase 1 (schema contract definition) is initialized with the following artifacts:

- `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`: canonical LinkML schema (`v1.0.0`).
- `src/nomad_plugins_metadata/schema_packages/datatractor_mapping.md`: compatibility mapping to datatractor fields.
- `src/nomad_plugins_metadata/adapters/nomad_mapping.md`: mapping to transitional `nomad-plugins` metainfo adapter.
- `src/nomad_plugins_metadata/examples/plugin-parser-minimal.yaml`: minimal parser plugin metadata example.
- `src/nomad_plugins_metadata/examples/plugin-app-minimal.yaml`: minimal app plugin metadata example.
- `src/nomad_plugins_metadata/examples/plugin-full-override.yaml`: comprehensive override-style example.

Design decisions:

1. Canonical source of truth is LinkML schema in this repository.
2. NOMAD metainfo classes in `src/nomad_plugins_metadata/schema_packages/schema_package.py` provide runtime integration and mirror the canonical model.
3. Extraction is owned by each plugin repository CI (not centralized in crawler CI).
4. `nomad-plugins` internal schema is transitional and should be phased out after migration gates.

## Schema validation

- Validate schema and examples:
  - `uv run python scripts/validate_schema_assets.py`
- Changelog for schema evolution:
  - `SCHEMA_CHANGELOG.md`

This `nomad` plugin was generated with `Cookiecutter` along with `@nomad`'s [`cookiecutter-nomad-plugin`](https://github.com/FAIRmat-NFDI/cookiecutter-nomad-plugin) template.

## Development

If you want to develop locally this plugin, clone the project and in the plugin folder, create a virtual environment (you can use Python 3.10, 3.11 or 3.12):
```sh
git clone https://github.com/FAIRmat-NFDI/nomad-plugins-metadata.git
cd nomad-plugins-metadata
python3.11 -m venv .pyenv
. .pyenv/bin/activate
```

Make sure to have `pip` upgraded:
```sh
pip install --upgrade pip
```

We recommend installing `uv` for fast pip installation of the packages:
```sh
pip install uv
```

Install the `nomad-lab` package:
```sh
uv pip install -e '.[dev]'
```

### Run the tests

You can run locally the tests:
```sh
python -m pytest -sv tests
```

where the `-s` and `-v` options toggle the output verbosity.

Our CI/CD pipeline produces a more comprehensive test report using the `pytest-cov` package. You can generate a local coverage report:
```sh
uv pip install pytest-cov
python -m pytest --cov=src tests
```

### Run linting and auto-formatting

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting the code. Ruff auto-formatting is also a part of the GitHub workflow actions. You can run locally:
```sh
ruff check .
ruff format . --check
```

### Debugging

For interactive debugging of the tests, use `pytest` with the `--pdb` flag. We recommend using an IDE for debugging, e.g., _VSCode_. If that is the case, add the following snippet to your `.vscode/launch.json`:
```json
{
  "configurations": [
      {
        "name": "<descriptive tag>",
        "type": "debugpy",
        "request": "launch",
        "cwd": "${workspaceFolder}",
        "program": "${workspaceFolder}/.pyenv/bin/pytest",
        "justMyCode": true,
        "env": {
            "_PYTEST_RAISE": "1"
        },
        "args": [
            "-sv",
            "--pdb",
            "<path-to-plugin-tests>",
        ]
    }
  ]
}
```

where `<path-to-plugin-tests>` must be changed to the local path to the test module to be debugged.

The settings configuration file `.vscode/settings.json` automatically applies the linting and formatting upon saving the modified file.

### Documentation on Github pages

To view the documentation locally, install the related packages using:
```sh
uv pip install -r requirements_docs.txt
```

Run the documentation server:
```sh
mkdocs serve
```

## Adding this plugin to NOMAD

Currently, NOMAD has two distinct flavors that are relevant depending on your role as an user:
1. [A NOMAD Oasis](#adding-this-plugin-in-your-nomad-oasis): any user with a NOMAD Oasis instance.
2. [Local NOMAD installation and the source code of NOMAD](#adding-this-plugin-in-your-local-nomad-installation-and-the-source-code-of-nomad): internal developers.

### Adding this plugin in your NOMAD Oasis

Read the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/oasis/plugins_install.html) for all details on how to deploy the plugin on your NOMAD instance.

### Adding this plugin in your local NOMAD installation and the source code of NOMAD

We now recommend using the dedicated [`nomad-distro-dev`](https://github.com/FAIRmat-NFDI/nomad-distro-dev) repository to simplify the process. Please refer to that repository for detailed instructions.

### Template update

We use [`cruft`](https://github.com/cruft/cruft) to update the project based on template changes. To run the check for updates locally, run `cruft update` in the root of the project. More details see the instructions on [`cruft` website](https://cruft.github.io/cruft/#updating-a-project).

## Main contributors
| Name | E-mail     |
|------|------------|
| Joseph Rudzinski | [joseph.rudzinski@physik.hu-berlin.de](mailto:joseph.rudzinski@physik.hu-berlin.de)
