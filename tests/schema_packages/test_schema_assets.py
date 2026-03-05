from nomad_plugins_metadata.schema_packages.schema_validation import (
    validate_schema_assets,
)


def test_schema_assets_validation():
    validate_schema_assets(run_linkml_validation=True)
