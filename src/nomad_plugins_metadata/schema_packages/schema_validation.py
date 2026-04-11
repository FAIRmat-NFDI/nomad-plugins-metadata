from __future__ import annotations

import subprocess
from importlib.resources import as_file, files

import yaml

from nomad_plugins_metadata.schema_packages.linkml_export import is_export_current

SCHEMA_RESOURCE = files('nomad_plugins_metadata.schema_packages').joinpath(
    'nomad_plugin_metadata.yaml'
)
EXAMPLES_RESOURCE = files('nomad_plugins_metadata').joinpath('examples')


def _run(cmd: list[str]) -> None:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        raise RuntimeError(
            f'Missing command: {cmd[0]!r}. Install dev dependencies first '
            '(e.g. `uv sync --all-extras`).'
        ) from exc
    if result.returncode != 0:
        raise RuntimeError(
            f'Command failed: {cmd}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}'
        )


def load_schema() -> dict:
    with SCHEMA_RESOURCE.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_schema_assets(run_linkml_validation: bool = True) -> None:
    if not is_export_current():
        raise RuntimeError(
            'LinkML schema is stale. Run: `uv run python scripts/export_linkml_schema.py`.'
        )

    schema = load_schema()

    schema_version = schema.get('version')
    if not schema_version:
        raise RuntimeError('Schema is missing top-level version.')

    domain_values = set(schema['enums']['DomainCategory']['permissible_values'].keys())
    maturity_values = set(schema['enums']['MaturityLevel']['permissible_values'].keys())

    examples = sorted(
        [
            example
            for example in EXAMPLES_RESOURCE.iterdir()
            if example.name.endswith('.yaml')
        ],
        key=lambda example: example.name,
    )
    if not examples:
        raise RuntimeError('No example files found in nomad_plugins_metadata/examples.')

    for example in examples:
        with example.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data.get('metadata_schema_version') != schema_version:
            raise RuntimeError(
                f'{example}: metadata_schema_version must equal schema version '
                f'({schema_version}).'
            )

        for usage in data.get('suggested_usages', []) or []:
            domain_category = usage.get('domain_category')
            if domain_category and domain_category not in domain_values:
                raise RuntimeError(
                    f'{example}: invalid domain_category {domain_category!r}. '
                    f'Allowed: {sorted(domain_values)}'
                )

            maturity = usage.get('maturity')
            if maturity and maturity not in maturity_values:
                raise RuntimeError(
                    f'{example}: invalid usage maturity {maturity!r}. '
                    f'Allowed: {sorted(maturity_values)}'
                )

    if run_linkml_validation:
        with as_file(SCHEMA_RESOURCE) as schema_path:
            for example in examples:
                with as_file(example) as example_path:
                    _run(
                        [
                            'linkml-validate',
                            '-s',
                            str(schema_path),
                            str(example_path),
                            '-C',
                            'PluginPackage',
                        ]
                    )
