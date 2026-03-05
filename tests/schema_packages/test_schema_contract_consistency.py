from pathlib import Path

import yaml

from nomad_plugins_metadata.schema_packages.schema_package import (
    DOMAIN_CATEGORIES,
    MATURITY_LEVELS,
)


def _load_linkml_schema():
    schema_path = (
        Path(__file__).resolve().parents[2]
        / 'src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml'
    )
    with schema_path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def test_domain_category_enum_consistency():
    schema = _load_linkml_schema()
    linkml_values = set(
        schema['enums']['DomainCategory']['permissible_values'].keys()
    )
    metainfo_values = set(DOMAIN_CATEGORIES)
    assert metainfo_values == linkml_values


def test_maturity_enum_consistency():
    schema = _load_linkml_schema()
    linkml_values = set(schema['enums']['MaturityLevel']['permissible_values'].keys())
    metainfo_values = set(MATURITY_LEVELS)
    assert metainfo_values == linkml_values
