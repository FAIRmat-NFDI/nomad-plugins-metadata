#!/usr/bin/env python3
"""Export LinkML schema from NOMAD metainfo source definitions."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nomad_plugins_metadata.schema_packages.linkml_export import (  # noqa: E402
    export_linkml_schema,
)


def main() -> None:
    export_linkml_schema()
    print('Exported LinkML schema from NOMAD metainfo source.')


if __name__ == '__main__':
    main()
