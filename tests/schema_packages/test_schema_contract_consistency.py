from nomad_plugins_metadata.schema_packages.schema_package import (
    DOMAIN_CATEGORIES,
    MATURITY_LEVELS,
)
from nomad_plugins_metadata.schema_packages.schema_validation import load_schema


def test_domain_category_enum_consistency():
    schema = load_schema()
    linkml_values = set(schema['enums']['DomainCategory']['permissible_values'].keys())
    metainfo_values = set(DOMAIN_CATEGORIES)
    assert metainfo_values == linkml_values


def test_maturity_enum_consistency():
    schema = load_schema()
    linkml_values = set(schema['enums']['MaturityLevel']['permissible_values'].keys())
    metainfo_values = set(MATURITY_LEVELS)
    assert metainfo_values == linkml_values
