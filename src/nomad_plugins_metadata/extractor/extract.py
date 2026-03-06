from __future__ import annotations

import re
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

import tomllib

from nomad_plugins_metadata.schema_packages.schema_validation import load_schema


def _read_pyproject(pyproject_path: Path) -> dict:
    if not pyproject_path.exists():
        return {}
    with pyproject_path.open('rb') as f:
        return tomllib.load(f)


def _schema_version() -> str:
    schema = load_schema()
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


def _normalize_package_name(name: str) -> str:
    return re.sub(r'[-_.]+', '-', name).lower().strip()


def _guess_capability_type(entry_point_name: str, python_object: str) -> str:
    text = f'{entry_point_name} {python_object}'.lower()
    for marker, capability in (
        ('schema', 'schema'),
        ('parser', 'parser'),
        ('normalizer', 'normalizer'),
        ('app', 'app'),
        ('example', 'example_upload'),
        ('api', 'api'),
        ('north', 'north_tool'),
    ):
        if marker in text:
            return capability
    return 'tool'


def _extract_extensions_from_name_regex(name_regex: str) -> list[str]:
    if not name_regex:
        return []
    # Best-effort parsing of regexes such as .*\\.(csv|xlsx)$ or ^.*\\.h5$
    matches = re.findall(r'\\\.([A-Za-z0-9]+)', name_regex)
    grouped = re.findall(r'\\\.\(([^)]+)\)', name_regex)
    for group in grouped:
        for candidate in group.split('|'):
            ext = candidate.strip()
            if re.fullmatch(r'[A-Za-z0-9]+', ext):
                matches.append(ext)
    seen = set()
    result = []
    for ext in matches:
        normalized = ext.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(f'.{normalized}')
    return result


def _extract_auxiliary_patterns_from_table(metadata_dict: dict | None) -> list[str]:
    if not metadata_dict:
        return []
    table = metadata_dict.get('tableOfFiles')
    if not isinstance(table, str) or not table.strip():
        return []
    candidates = re.findall(r'`([^`]+)`', table)
    result = []
    seen = set()
    for candidate in candidates:
        value = candidate.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _extract_schema_dependencies(pyproject: dict) -> list[dict]:
    project = pyproject.get('project', {}) or {}
    dependencies = []

    def add_dependency(dep_string: str, optional: bool) -> None:
        dep = dep_string.strip()
        if not dep:
            return
        match = re.match(r'^\s*([A-Za-z0-9_.-]+)\s*(.*)$', dep)
        if not match:
            return
        name = match.group(1)
        version_range = match.group(2).strip()
        dependencies.append(
            {
                'dependency_type': 'python_package',
                'package_name': name,
                'version_range': version_range or '',
                'optional': optional,
                'purpose': 'runtime' if not optional else 'optional',
            }
        )

    for dep in project.get('dependencies', []) or []:
        add_dependency(str(dep), optional=False)

    for _, deps in (project.get('optional-dependencies', {}) or {}).items():
        for dep in deps or []:
            add_dependency(str(dep), optional=True)

    return dependencies


def _entry_point_type_to_capability(entry_point_type: str | None) -> str:
    mapping = {
        'schema_package': 'schema',
        'parser': 'parser',
        'normalizer': 'normalizer',
        'app': 'app',
        'example_upload': 'example_upload',
        'api': 'api',
        'north_tool': 'north_tool',
    }
    if entry_point_type is None:
        return 'tool'
    return mapping.get(entry_point_type, entry_point_type)


def _discover_installed_nomad_entry_points(
    target_package_names: set[str],
) -> dict[str, object]:
    discovered: dict[str, object] = {}
    try:
        entry_points = metadata.entry_points(group='nomad.plugin')
    except Exception:
        return discovered

    for entry_point in entry_points:
        dist = getattr(entry_point, 'dist', None)
        dist_name = getattr(dist, 'name', None)
        if not dist_name:
            continue
        if _normalize_package_name(str(dist_name)) not in target_package_names:
            continue
        try:
            loaded = entry_point.load()
        except Exception:
            continue
        discovered[entry_point.name] = loaded

    return discovered


def _build_entry_points_and_capabilities(
    project: dict,
    repo_path: Path,
) -> tuple[list[dict], list[dict], list[str], list[dict]]:
    pyproject_entry_points = (
        (project.get('entry-points', {}) or {}).get('nomad.plugin', {}) or {}
    )
    package_name = str(project.get('name', repo_path.name))
    target_packages = {
        _normalize_package_name(package_name),
        _normalize_package_name(repo_path.name),
    }
    installed_entry_points = _discover_installed_nomad_entry_points(target_packages)

    entry_points: list[dict] = []
    capabilities: list[dict] = []
    supported_filetypes: list[str] = []
    file_format_support: list[dict] = []

    for ep_name, python_object in pyproject_entry_points.items():
        loaded = installed_entry_points.get(ep_name)
        entry_point_type = getattr(loaded, 'entry_point_type', None)
        capability_type = _entry_point_type_to_capability(entry_point_type)
        if capability_type == entry_point_type:
            capability_type = _guess_capability_type(ep_name, str(python_object))

        entry_points.append(
            {
                'id': f'nomad.plugin:{ep_name}',
                'entry_point_group': 'nomad.plugin',
                'entry_point_name': ep_name,
                'python_object': str(python_object),
                'capability_type': capability_type,
            }
        )

        capability = {
            'id': str(getattr(loaded, 'id', ep_name)),
            'capability_type': capability_type,
            'title': str(getattr(loaded, 'name', ep_name)),
            'summary': str(getattr(loaded, 'description', '') or ''),
        }

        if capability_type == 'parser':
            parser_details = {
                'parser_name': str(getattr(loaded, 'name', ep_name)),
                'mainfile_name_re': str(getattr(loaded, 'mainfile_name_re', '') or ''),
                'mainfile_contents_re': str(
                    getattr(loaded, 'mainfile_contents_re', '') or ''
                ),
                'mainfile_mime_re': str(getattr(loaded, 'mainfile_mime_re', '') or ''),
                'mainfile_binary_header': str(
                    getattr(loaded, 'mainfile_binary_header', '') or ''
                ),
                'compression_support': list(
                    getattr(loaded, 'supported_compressions', []) or []
                ),
                'auxiliary_file_patterns': _extract_auxiliary_patterns_from_table(
                    getattr(loaded, 'metadata', None)
                ),
            }
            parser_details = {
                key: value
                for key, value in parser_details.items()
                if value not in ('', [], None)
            }
            if parser_details:
                capability['parser_details'] = parser_details

            extensions = _extract_extensions_from_name_regex(
                str(getattr(loaded, 'mainfile_name_re', '') or '')
            )
            for ext in extensions:
                if ext in supported_filetypes:
                    continue
                supported_filetypes.append(ext)
                mime = str(getattr(loaded, 'mainfile_mime_re', '') or '')
                file_format_support.append(
                    {
                        'id': ext.lstrip('.'),
                        'label': ext,
                        'extensions': [ext],
                        'mime_types': [mime] if mime else [],
                    }
                )

        capability = {
            key: value for key, value in capability.items() if value not in ('', [], None)
        }
        capabilities.append(capability)

    return entry_points, capabilities, supported_filetypes, file_format_support


def build_generated_metadata(repo_path: Path) -> dict:
    """Generate baseline metadata from repo-local static sources."""
    return build_generated_metadata_with_release_context(
        repo_path=repo_path, release_tag=None, release_sha=None
    )


def build_generated_metadata_with_release_context(
    repo_path: Path,
    release_tag: str | None,
    release_sha: str | None,
) -> dict:
    """Generate baseline metadata from repo-local static sources."""
    pyproject = _read_pyproject(repo_path / 'pyproject.toml')
    project = pyproject.get('project', {})
    urls = project.get('urls', {}) or {}
    entry_points, capabilities, supported_filetypes, file_format_support = (
        _build_entry_points_and_capabilities(project, repo_path)
    )
    schema_dependencies = _extract_schema_dependencies(pyproject)

    license_value = ''
    license_data = project.get('license')
    if isinstance(license_data, str):
        license_value = license_data
    elif isinstance(license_data, dict):
        license_value = str(
            license_data.get('text', '')
            or license_data.get('file', '')
            or license_data.get('name', '')
        )

    package_name = project.get('name', repo_path.name)
    issue_tracker = ''
    for key in urls:
        if key.lower().replace(' ', '').replace('_', '') in (
            'issuetracker',
            'bugtracker',
        ):
            issue_tracker = str(urls[key])
            break

    metadata = {
        'id': package_name,
        'metadata_schema_version': _schema_version(),
        'name': package_name,
        'description': project.get('description', ''),
        'plugin_version': project.get('version', ''),
        'license': license_value,
        'upstream_repository': urls.get('Repository', ''),
        'documentation': urls.get('Documentation', ''),
        'homepage': urls.get('Homepage', ''),
        'issue_tracker': issue_tracker,
        'maintainers': _owners_to_maintainers(project),
        'entry_points': entry_points,
        'capabilities': capabilities,
        'supported_filetypes': supported_filetypes,
        'file_format_support': file_format_support,
        'schema_dependencies': schema_dependencies,
        'metadata_provenance': [
            {
                'source': 'pyproject',
                'extraction_method': 'deterministic',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'generator_version': '0.1.0',
            },
            {
                'source': 'plugin_entry_points',
                'extraction_method': 'deterministic',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'generator_version': '0.1.0',
            }
        ],
    }
    clean_release_tag = (release_tag or '').strip()
    clean_release_sha = (release_sha or '').strip()
    if clean_release_tag or clean_release_sha:
        metadata['release_context'] = {
            'release_tag': clean_release_tag,
            'release_commit_sha': clean_release_sha,
        }

    # Drop empty values for cleaner generated files.
    return {k: v for k, v in metadata.items() if v not in ('', [], None)}
