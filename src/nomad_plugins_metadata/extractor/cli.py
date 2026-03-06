from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import yaml

from nomad_plugins_metadata.extractor.extract import (
    build_generated_metadata_with_release_context,
)
from nomad_plugins_metadata.extractor.merge import merge_generated_and_manual
from nomad_plugins_metadata.schema_packages.schema_validation import load_schema


@dataclass(frozen=True)
class ExtractRunConfig:
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


def _slot_template(slot_name: str, schema: dict, seen: set[str]):
    slots = schema.get('slots', {}) or {}
    classes = schema.get('classes', {}) or {}
    slot = slots.get(slot_name, {}) or {}
    range_name = slot.get('range', 'string')
    is_multivalued = bool(slot.get('multivalued', False))
    is_class_range = range_name in classes

    if is_multivalued:
        if is_class_range:
            return [_class_template(range_name, schema, seen)]
        return []

    if is_class_range:
        return _class_template(range_name, schema, seen)
    return None


def _class_template(class_name: str, schema: dict, seen: set[str]):
    if class_name in seen:
        return {}
    seen_next = set(seen)
    seen_next.add(class_name)
    classes = schema.get('classes', {}) or {}
    cls = classes.get(class_name, {}) or {}
    result = {}
    for slot_name in cls.get('slots', []) or []:
        result[slot_name] = _slot_template(slot_name, schema, seen_next)
    return result


def _build_manual_template() -> dict:
    schema = load_schema()
    return _class_template('PluginPackage', schema, seen=set())


def run_extract(repo_path: Path, config: ExtractRunConfig) -> None:
    auto = build_generated_metadata_with_release_context(
        repo_path=repo_path,
        release_tag=config.release_tag,
        release_sha=config.release_sha,
    )
    if not config.manual_path.exists() and config.create_manual_template_if_missing:
        _write_yaml(config.manual_path, _build_manual_template())

    manual = _load_yaml(config.manual_path)
    manual_non_empty = _prune_empty(manual)
    effective, report = merge_generated_and_manual(auto, manual_non_empty)

    _write_yaml(config.auto_path, auto)
    _write_yaml(config.effective_path, effective)
    _write_yaml(config.report_path, report)


def build_parser() -> argparse.ArgumentParser:
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
        '--manual-path', type=Path, default=Path('nomad_plugin_metadata.manual.yaml')
    )
    extract.add_argument(
        '--auto-path',
        type=Path,
        default=Path('nomad_plugin_metadata.auto.yaml'),
    )
    extract.add_argument(
        '--effective-path',
        type=Path,
        default=Path('nomad_plugin_metadata.yaml'),
    )
    extract.add_argument(
        '--report-path',
        type=Path,
        default=Path('.nomad/plugin-metadata.override-report.yaml'),
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
        help='Create nomad_plugin_metadata.manual.yaml template when manual file is missing.',
    )

    return parser


def main() -> None:
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
