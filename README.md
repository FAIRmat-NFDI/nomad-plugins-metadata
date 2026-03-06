# nomad-plugins-metadata

Canonical schema + tooling package for generating, validating, and merging NOMAD plugin metadata.

## What this package provides

- Canonical metadata schema:
  - `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`
- NOMAD metainfo adapter classes:
  - `src/nomad_plugins_metadata/schema_packages/schema_package.py`
- Mapping docs:
  - `src/nomad_plugins_metadata/schema_packages/datatractor_mapping.md`
  - `src/nomad_plugins_metadata/adapters/nomad_mapping.md`
- Reusable extractor CLI:
  - `nomad-plugin-metadata extract ...`
- Reusable GitHub workflow for plugin repos:
  - `.github/workflows/extract-plugin-metadata.yml`

## Typical usage in a plugin repository

1. Maintain manual metadata in:
   - `nomad_plugin_metadata.yaml`
2. On release publish, run extractor automation via reusable workflow in PR mode.
3. Automation generates:
   - `.nomad/plugin-metadata.generated.yaml`
   - `.nomad/plugin-metadata.effective.yaml`
   - `.nomad/plugin-metadata.override-report.yaml`
4. In PR mode, workflow also updates:
   - `nomad_plugin_metadata.yaml` (forward-facing file)
5. Merge precedence is deterministic:
   - manual override (`nomad_plugin_metadata.yaml`) > generated metadata
6. Generated/effective metadata include release linkage:
   - `release_context.release_tag`
   - `release_context.release_commit_sha`

## Schema validation

- Validate schema and examples:
  - `uv run python scripts/validate_schema_assets.py`
- Changelog for schema evolution:
  - `SCHEMA_CHANGELOG.md`

## Extractor CLI

This package now includes a reusable extractor CLI for plugin repositories:

```sh
nomad-plugin-metadata extract --repo-path .
```

Default outputs:

- `.nomad/plugin-metadata.generated.yaml` (machine-generated baseline)
- `.nomad/plugin-metadata.effective.yaml` (deep-merged effective metadata)
- `.nomad/plugin-metadata.override-report.yaml` (manual override report/warnings)

Merge precedence is deterministic: `nomad_plugin_metadata.yaml` (manual) > generated.

## Reusable Workflow

This repository provides a reusable workflow that plugin repos can call:
`.github/workflows/extract-plugin-metadata.yml`.

Ready-to-copy caller template:
`docs/templates/update-plugin-metadata.yml`
and PR check template:
`docs/templates/check-plugin-metadata-pr.yml`

This repository also uses the same pattern for self-testing:
`.github/workflows/update-plugin-metadata.yml`

Example caller workflow in a plugin repository:

```yaml
name: update-plugin-metadata

on:
  release:
    types: [published]
  workflow_dispatch:

jobs:
  extract:
    uses: FAIRmat-NFDI/nomad-plugins-metadata/.github/workflows/extract-plugin-metadata.yml@main
    permissions:
      contents: write
      pull-requests: write
    with:
      package_spec: nomad-plugins-metadata==0.1.0
      check_only: false
      auto_commit: false
      create_pr: true
      release_tag: ${{ github.event.release.tag_name || '' }}
      release_sha: ${{ github.sha }}
```

For PR check-only enforcement (no auto-commit), use the template at
`docs/templates/check-plugin-metadata-pr.yml`. If metadata is out of sync, the workflow fails with remediation commands in the job summary.

Release PR mode (`create_pr: true`) behavior:

- writes `.nomad/plugin-metadata.generated.yaml`
- writes `.nomad/plugin-metadata.effective.yaml`
- overwrites `.nomad/plugin-metadata.override-report.yaml`
- updates forward-facing `nomad_plugin_metadata.yaml`
- creates/updates a single rolling PR branch with a standard body including release tag/sha and changed files

If you need plugin-specific enrichment, add a repository-local hook script and run it before/after the reusable extractor job.

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
