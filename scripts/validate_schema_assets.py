#!/usr/bin/env python3
"""Validate canonical schema assets and examples."""

from nomad_plugins_metadata.schema_packages.schema_validation import (
    validate_schema_assets,
)


def main() -> None:
    validate_schema_assets(run_linkml_validation=True)
    print('Schema assets and examples validated successfully.')


if __name__ == '__main__':
    main()
