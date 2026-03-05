from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import tomllib

from nomad_plugins_metadata.schema_packages.schema_validation import SCHEMA_PATH


def _read_pyproject(pyproject_path: Path) -> dict:
    if not pyproject_path.exists():
        return {}
    with pyproject_path.open('rb') as f:
        return tomllib.load(f)


def _schema_version() -> str:
    import yaml

    with SCHEMA_PATH.open('r', encoding='utf-8') as f:
        schema = yaml.safe_load(f)
    return str(schema.get('version', '1.0.0'))


def _owners_to_maintainers(project: dict) -> list[dict]:
    maintainers = []
    for key in ('maintainers', 'authors'):
        for item in project.get(key, []) or []:
            name = item.get('name')
            email = item.get('email')
            if not name and not email:
                continue
            maintainers.append({'name': name or '', 'email': email or ''})
    # preserve order, deduplicate exact dicts
    deduped = []
    seen = set()
    for entry in maintainers:
        marker = (entry.get('name', ''), entry.get('email', ''))
        if marker in seen:
            continue
        seen.add(marker)
        deduped.append(entry)
    return deduped


def build_generated_metadata(repo_path: Path) -> dict:
    """Generate baseline metadata from repo-local static sources."""
    pyproject = _read_pyproject(repo_path / 'pyproject.toml')
    project = pyproject.get('project', {})
    urls = project.get('urls', {}) or {}

    package_name = project.get('name', repo_path.name)
    metadata = {
        'id': package_name,
        'metadata_schema_version': _schema_version(),
        'name': package_name,
        'description': project.get('description', ''),
        'plugin_version': project.get('version', ''),
        'source_repository': urls.get('Repository', ''),
        'maintainers': _owners_to_maintainers(project),
        'metadata_provenance': [
            {
                'source': 'pyproject',
                'extraction_method': 'deterministic',
                'confidence': 0.9,
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'generator_version': '0.1.0',
            }
        ],
    }

    # Drop empty values for cleaner generated files.
    return {k: v for k, v in metadata.items() if v not in ('', [], None)}
