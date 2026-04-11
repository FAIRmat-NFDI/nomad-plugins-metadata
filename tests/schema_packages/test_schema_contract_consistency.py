from nomad_plugins_metadata.schema_packages import schema_package as sp
from nomad_plugins_metadata.schema_packages.linkml_export import (
    generate_linkml_schema,
    is_export_current,
)
from nomad_plugins_metadata.schema_packages.schema_validation import load_schema


def test_linkml_export_is_current():
    assert is_export_current()


def test_generated_schema_matches_committed_schema():
    assert generate_linkml_schema() == load_schema()


def test_enum_consistency_between_nomad_and_linkml():
    schema = load_schema()
    expected = {
        'CapabilityType': set(sp.CAPABILITY_TYPES),
        'DomainCategory': set(sp.DOMAIN_CATEGORIES),
        'MaturityLevel': set(sp.MATURITY_LEVELS),
        'DependencyType': set(sp.DEPENDENCY_TYPES),
        'MetadataSource': set(sp.METADATA_SOURCES),
        'ExtractionMethod': set(sp.EXTRACTION_METHODS),
        'CompressionType': set(sp.COMPRESSION_TYPES),
    }
    for enum_name, enum_values in expected.items():
        exported_values = set(schema['enums'][enum_name]['permissible_values'].keys())
        assert exported_values == enum_values
