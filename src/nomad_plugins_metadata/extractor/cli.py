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
    manual_path: Path
    generated_path: Path
    effective_path: Path
    report_path: Path
    release_tag: str | None = None
    release_sha: str | None = None
    update_front_file: Path | None = None


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


def run_extract(repo_path: Path, config: ExtractRunConfig) -> None:
    generated = build_generated_metadata_with_release_context(
        repo_path=repo_path,
        release_tag=config.release_tag,
        release_sha=config.release_sha,
    )
    manual = _load_yaml(config.manual_path)
    effective, report = merge_generated_and_manual(generated, manual)

    _write_yaml(config.generated_path, generated)
    _write_yaml(config.effective_path, effective)
    _write_yaml(config.report_path, report)
    if config.update_front_file is not None:
        _write_yaml(config.update_front_file, effective)


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
        '--manual-path', type=Path, default=Path('nomad_plugin_metadata.yaml')
    )
    extract.add_argument(
        '--generated-path',
        type=Path,
        default=Path('.nomad/plugin-metadata.generated.yaml'),
    )
    extract.add_argument(
        '--effective-path',
        type=Path,
        default=Path('.nomad/plugin-metadata.effective.yaml'),
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
        '--update-front-file',
        type=Path,
        default=None,
        help='Optional path to overwrite with effective metadata (e.g. nomad_plugin_metadata.yaml).',
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == 'extract':
        run_extract(
            repo_path=args.repo_path,
            config=ExtractRunConfig(
                manual_path=args.manual_path,
                generated_path=args.generated_path,
                effective_path=args.effective_path,
                report_path=args.report_path,
                release_tag=args.release_tag or None,
                release_sha=args.release_sha or None,
                update_front_file=args.update_front_file,
            ),
        )


if __name__ == '__main__':
    main()
