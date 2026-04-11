#!/usr/bin/env python3
"""Validate canonical schema assets and examples."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nomad_plugins_metadata.schema_packages.schema_validation import (  # noqa: E402, I001
    validate_schema_assets,
)


def main() -> None:
    validate_schema_assets(run_linkml_validation=True)
    print('Schema assets and examples validated successfully.')


if __name__ == '__main__':
    main()
