from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = (
    REPO_ROOT / 'src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml'
)
EXAMPLES_DIR = REPO_ROOT / 'src/nomad_plugins_metadata/examples'


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


def validate_schema_assets(run_linkml_validation: bool = True) -> None:
    with SCHEMA_PATH.open('r', encoding='utf-8') as f:
        schema = yaml.safe_load(f)

    schema_version = schema.get('version')
    if not schema_version:
        raise RuntimeError('Schema is missing top-level version.')

    domain_values = set(schema['enums']['DomainCategory']['permissible_values'].keys())
    maturity_values = set(schema['enums']['MaturityLevel']['permissible_values'].keys())

    examples = sorted(EXAMPLES_DIR.glob('*.yaml'))
    if not examples:
        raise RuntimeError(
            'No example files found in src/nomad_plugins_metadata/examples.'
        )

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
        for example in examples:
            _run(
                [
                    'linkml-validate',
                    '-s',
                    str(SCHEMA_PATH),
                    str(example),
                    '-C',
                    'PluginPackage',
                ]
            )
