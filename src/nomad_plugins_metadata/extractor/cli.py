from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import yaml

from nomad_plugins_metadata.extractor.extract import (
    build_generated_metadata_with_release_context,
)
from nomad_plugins_metadata.extractor.merge import merge_generated_and_manual


@dataclass(frozen=True)
class ExtractRunConfig:
    """Runtime configuration for one extraction run."""

    manual_path: Path
    auto_path: Path
    effective_path: Path
    report_path: Path
    release_tag: str | None = None
    release_sha: str | None = None
    create_manual_template_if_missing: bool = True


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f'Expected mapping at {path}, got {type(data).__name__}.')
    return data


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, sort_keys=False)


def _is_empty(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ''
    if isinstance(value, list):
        return len(value) == 0
    if isinstance(value, dict):
        return len(value) == 0
    return False


def _prune_empty(value):
    if isinstance(value, dict):
        pruned = {}
        for key, nested in value.items():
            nested_pruned = _prune_empty(nested)
            if _is_empty(nested_pruned):
                continue
            pruned[key] = nested_pruned
        return pruned
    if isinstance(value, list):
        pruned_items = []
        for item in value:
            item_pruned = _prune_empty(item)
            if _is_empty(item_pruned):
                continue
            pruned_items.append(item_pruned)
        return pruned_items
    return value


def _manual_template_text() -> str:
    return """# Maintainer-owned metadata overrides and manual additions.
# This file is never machine-overwritten after creation.
# Use null/empty values as placeholders; only non-empty values override auto output.
# list[str] domain/topic tags (e.g. "simulations", "spectroscopy")
subject: []
# enum {alpha, beta, stable, archived}
maturity: null
# str, e.g. "main"
repository_default_branch: null

# Deployment flags.
deployment:
  # boolean
  on_central: null
  # boolean
  on_example_oasis: null
  # boolean
  on_pypi: null
  # str (PyPI package name)
  pypi_package: null

# Suggested usages for registry filtering/discovery.
suggested_usages:
  -
    # str (stable ID slug), e.g. "parse-xrd-patterns"
    id: null
    # str
    title: null
    # str (what user wants to do), e.g. "Import and parse raw files"
    user_intent: null
    # enum {simulations, measurements, synthesis, cross-domain, workflow, infrastructure}
    domain_category: null
    # str, e.g. "XRD", "DFT"
    technique: null
    # str, e.g. "beginner", "expert"
    audience: null
    # enum {alpha, beta, stable, archived}
    maturity: null
    # list[str]
    tags: []

# Optional file format metadata enrichments.
file_format_support:
  -
    # str (stable ID), e.g. "csv"
    id: null
    # str display label, e.g. ".csv"
    label: null
    # list[str] extensions including dot, e.g. [".csv", ".txt"]
    extensions: []
    # list[str], e.g. ["text/csv"]
    mime_types: []
    # str, e.g. "CIF", "NeXus"
    standard: null
    # str, instrument or context label
    instrument_context: null
    # str free text notes
    notes: null
"""


def _write_manual_template(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_manual_template_text(), encoding='utf-8')


def run_extract(repo_path: Path, config: ExtractRunConfig) -> None:
    """Generate auto metadata and materialize merged/report artifacts.

    The resulting precedence is deterministic:
    non-empty manual values override generated values.
    """
    auto = build_generated_metadata_with_release_context(
        repo_path=repo_path,
        release_tag=config.release_tag,
        release_sha=config.release_sha,
    )
    if not config.manual_path.exists() and config.create_manual_template_if_missing:
        _write_manual_template(config.manual_path)

    manual = _load_yaml(config.manual_path)
    manual_non_empty = _prune_empty(manual)
    effective, report = merge_generated_and_manual(auto, manual_non_empty)

    _write_yaml(config.auto_path, auto)
    _write_yaml(config.effective_path, effective)
    _write_yaml(config.report_path, report)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser for `nomad-plugin-metadata`."""
    parser = argparse.ArgumentParser(
        prog='nomad-plugin-metadata',
        description='Generate and merge NOMAD plugin metadata files.',
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    extract = subparsers.add_parser(
        'extract', help='Generate metadata files for a repo.'
    )
    extract.add_argument('--repo-path', type=Path, default=Path('.'))
    extract.add_argument(
        '--manual-path',
        type=Path,
        default=Path('.metadata/nomad_plugin_metadata.manual.yaml'),
    )
    extract.add_argument(
        '--auto-path',
        type=Path,
        default=Path('.metadata/nomad_plugin_metadata.auto.yaml'),
    )
    extract.add_argument(
        '--effective-path',
        type=Path,
        default=Path('nomad_plugin_metadata.yaml'),
    )
    extract.add_argument(
        '--report-path',
        type=Path,
        default=Path('.metadata/plugin-metadata.override-report.yaml'),
    )
    extract.add_argument(
        '--release-tag',
        type=str,
        default='',
        help='Release tag to embed in generated/effective metadata.',
    )
    extract.add_argument(
        '--release-sha',
        type=str,
        default='',
        help='Release commit SHA to embed in generated/effective metadata.',
    )
    extract.add_argument(
        '--create-manual-template-if-missing',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='Create .metadata/nomad_plugin_metadata.manual.yaml template when manual file is missing.',
    )

    return parser


def main() -> None:
    """CLI entrypoint."""
    args = build_parser().parse_args()
    if args.command == 'extract':
        run_extract(
            repo_path=args.repo_path,
            config=ExtractRunConfig(
                manual_path=args.manual_path,
                auto_path=args.auto_path,
                effective_path=args.effective_path,
                report_path=args.report_path,
                release_tag=args.release_tag or None,
                release_sha=args.release_sha or None,
                create_manual_template_if_missing=args.create_manual_template_if_missing,
            ),
        )


if __name__ == '__main__':
    main()
